Generate unit tests for One API endpoint.

Rules:
- Cover success and failure cases
- Mock external dependencies
- Use NUnit and dependency packages
- If jwt token is required, take it from constant file
- Follow existing test class structure and naming conventions

Input:
- Controller + service code

Output:
- Test class
example:Input:
Endpoint Summary:
Controller Code:
[HttpGet("underwriter")]
[
    SwaggerOperation(Tags = new[] { "Underwriter" }),
    EndpointSummary("Retrieves comprehensive bond information for the Underwriter Review Screen by aggregating data from WSBND and WSQAP systems"),
    ProducesResponseType(typeof(UnderwriterInformationResponse), 200),
    ProducesResponseType(typeof(NotFoundResult), 404)
]
public async Task<ActionResult<UnderwriterInformationResponse>> GetUnderwriter(
    [
        FromQuery(Name = "bond_number"),
        Required,
        RegularExpression(UfgRegex.Surety.BondNumber),
        SwaggerDefault("54232925")
    ]
    string bondNumber
)
{
    return Ok(await underwriterProvider.GetUnderwriterInformation(bondNumber));
}
Service Code:
public async Task<UnderwriterInformationResponse> GetUnderwriterInformation(string bondNumber)
{
    var underwriterResponse = await GetUnderwriterInfoParallel(bondNumber);

	// Verify that the agency access process has been removed, as it is now implemented in the XAPI layer by Bowersox, Tom.

	var inquiryResponse = await GetInquiryData(bondNumber);

    return MapToUnderwriterInformationResponse(underwriterResponse, inquiryResponse);
}

private async Task<UnderWriterResponse> GetUnderwriterInfoParallel(string bondNumber)
{
    var taskW = bondProvider.GetBondUnderwriterInfoWithPrefixResponse(bondNumber, "W");
    var task5 = bondProvider.GetBondUnderwriterInfoWithPrefixResponse(bondNumber, "5");

	await Task.WhenAll(taskW, task5);

    if (taskW.Result != null)
        return taskW.Result;

    if (task5.Result != null)
        return task5.Result;

    throw new HttpResponseException(
        HttpStatusCode.NotFound,
        new ErrorResponse
        {
            Message = $"Bond not found for bond number: {bondNumber}",
            ErrorCode = "404"
        }
    );
}

private async Task<QuickInquiryResponse?> GetInquiryData(string bondNumber)
{
    using var suretySystemClient = apiConfig.GetSuretySystemClient();
    try
    {
        var response = await suretySystemClient.GetAsync<QuickInquiryResponse>(
            $"inquiry?bond_number={bondNumber}",
            useSnakeCase: true
        );
        return response;
    }
    catch (HttpResponseException ex) when (ex.Response.StatusCode == HttpStatusCode.NotFound)
    {
        return null;
    }
    catch (HttpResponseException)
    {
        throw;
    }
}

private static UnderwriterInformationResponse MapToUnderwriterInformationResponse(
    UnderWriterResponse underwriterResponse,
    QuickInquiryResponse? inquiryResponse)
{
    var currentDate = DateOnly.FromDateTime(DateTime.UtcNow);
    var bondStatus = (underwriterResponse.ClosedDate, underwriterResponse.ExpirationDate) switch
    {
        ({ } closedDate, _) when closedDate != DateOnly.MinValue => "Closed",
        (_, var expirationDate) when currentDate >= expirationDate => "Expired",
        _ => "Open"
    };

    return new UnderwriterInformationResponse
    {
        EffectiveDate = underwriterResponse?.EffectiveDate,
        BondFormType = underwriterResponse?.BondFormType,
        FormNumber = underwriterResponse?.FormNumber,
        BondState = inquiryResponse?.BondState,
        BondZip = inquiryResponse?.BondZip,
        BondDescription = underwriterResponse?.BondDescription,
        ObligeeName = underwriterResponse?.ObligeeName,
        ObligeeStreetAddress = underwriterResponse?.ObligeeStreetAddress,
        ObligeeStreetAddress2 = underwriterResponse?.ObligeeStreetAddress2,
        ObligeeCityStateZip = underwriterResponse?.ObligeeCityStateZip,
        ObligeePhone = underwriterResponse?.ObligeePhone,
        MaintenancePeriod = underwriterResponse?.MaintenancePeriod,
        ContractDate = underwriterResponse?.ContractDate,
        ContractAmount = underwriterResponse?.ContractAmount,
        BondPremium = underwriterResponse?.BondPremium,
        BidDate = underwriterResponse?.BidDate,
        BidPercent = underwriterResponse?.BidPercent,
        BidAmount = underwriterResponse?.BidAmount,
        AccountNumber = underwriterResponse?.AccountNumber,
        AccountName = underwriterResponse?.AccountName,
        AccountStreetAddress = underwriterResponse?.AccountStreetAddress,
        AccountCity = underwriterResponse?.AccountCity,
        AccountState = underwriterResponse?.AccountState,
        AccountZip = underwriterResponse?.AccountZip,
        AgencyNumber = underwriterResponse?.AgencyNumber,
        ProducerNumber = underwriterResponse?.ProducerNumber,
        BondType = underwriterResponse?.BondType,
        CompletionDate = inquiryResponse?.CompletionDate,
        IsRenewableAfterYear = inquiryResponse?.IsRenewableAfterYear,
        LiquidatedDamages = inquiryResponse?.LiquidatedDamages,
        SecondLowestBidder = inquiryResponse?.SecondLowestBidder,
        BidEstimate = inquiryResponse?.BidEstimate,
        TypeOfBond = inquiryResponse?.TypeOfBond,
        BondCity = inquiryResponse?.BondCity,
        BondStatusShort = underwriterResponse?.BondStatusShort,
        BondStatus = bondStatus
    };
}
Expected Output:
using Microsoft.Extensions.DependencyInjection;
using Moq;
using System.Net;
using UFG.Contract.API.DTOs.PAPI.Surety;
using UFG.Contract.API.DTOs.SAPI.Surety;
using UFG.Contract.API.Types.Common.Rest;
using UFG.Service.API.Core.Handlers;
using UFG.Service.API.Test.Common;
using UFG.Service.API.Test.Common.Common;
using UFG.Service.PAPI.Surety.Config;
using UFG.Service.PAPI.Surety.Controllers;

namespace UFG.Service.PAPI.Surety.Tests.Endpoints
{
	public class GetUnderwriterTests
	{
		private IServiceProvider _serviceProvider;
		private Mock<ApiConfigWrapper> _mockApiConfigWrapper;
		private Mock<IWebserviceHttpClient> _mockWebserviceHttpClient;

		[SetUp]
		public void Setup()
		{
			(_serviceProvider, _mockApiConfigWrapper) = BootstrapperSetup.SetupServiceCollection();
			_mockWebserviceHttpClient = new Mock<IWebserviceHttpClient>();
			_mockApiConfigWrapper.Setup(_ => _.GetSuretySystemClient()).Returns(_mockWebserviceHttpClient.Object);
			_mockApiConfigWrapper.Setup(_ => _.GetDateTimeNow).Returns(DateTime.UtcNow);
		}

		[TearDown]
		public void TearDown()
		{
			(_serviceProvider as IDisposable)?.Dispose();
			_mockApiConfigWrapper.Reset();
		}

		private SuretyController GetSuretyController()
		{
			var controller = _serviceProvider.GetRequiredService<SuretyController>();
			return controller;
		}

		[Test]
		public async Task GetUnderwriter_Pass()
		{	
			_mockWebserviceHttpClient
				.Setup(_ => _.GetAsync<UnderWriterResponse>(It.Is<string>(s => s.Contains("under-writer?bond_number=")), true))
				.ReturnsAsync(BondNumberUnderwriterResponse);

			_mockWebserviceHttpClient
				.Setup(_ => _.GetAsync<QuickInquiryResponse>(It.Is<string>(s => s.Contains("inquiry?bond_number=")), true))
				.ThrowsAsync(new HttpResponseException(System.Net.HttpStatusCode.NotFound, new ErrorResponse
				{
					Message = "BONDF RECORD NOT FOUND",
					ErrorCode = "210"
				}));

			
			var controller = GetSuretyController();
			var actualResponse = await controller.GetUnderwriter("54232925");
			TestResultValidation.Validate200Response(UnderwriterSuccessResponse, actualResponse);			
		}

		[Test]
		public async Task GetUnderwriter_EmptyResponse()
		{
			_mockWebserviceHttpClient
				.Setup(_ => _.GetAsync<UnderWriterResponse>(
					It.Is<string>(s => s.Contains("under-writer?bond_number")),
					true))
				.ThrowsAsync(new HttpResponseException(System.Net.HttpStatusCode.NotFound,new ErrorResponse { Message = "Not Found"}));

			_mockWebserviceHttpClient
				.Setup(_ => _.GetAsync<QuickInquiryResponse>(It.Is<string>(s => s.Contains("inquiry?bond_number=")), true))
				.ThrowsAsync(new HttpResponseException(System.Net.HttpStatusCode.NotFound, new ErrorResponse
				{
					Message = "BONDF RECORD NOT FOUND",
					ErrorCode = "210"
				}));

			var response = new UnderwriterInformationResponse();
			var controller = GetSuretyController();
			var expected = new ErrorResponse { Message = "Bond not found for bond number: 54232925", ErrorCode = "404" };
			
			await TestResultValidation.ValidateErrorResponse(
				async () => await controller.GetUnderwriter("54232925"),
				expected,
				HttpStatusCode.NotFound
			);
		}

		private static UnderWriterResponse BondNumberUnderwriterResponse =>
			ReadJsonIntoObject.Read<UnderWriterResponse>("TestData/GetUnderwriter/Bondnumberwith5Response.json")
					?? throw new NullReferenceException("Failed to deserialize TestData/GetUnderwriter/Bondnumberwith5Response.json");

		private static UnderwriterInformationResponse UnderwriterSuccessResponse =>
			ReadJsonIntoObject.Read<UnderwriterInformationResponse>("TestData/GetUnderwriter/UnderwriterSuccessResponse.json")
			?? throw new NullReferenceException("Failed to deserialize TestData/GetUnderwriter/UnderwriterSuccessResponse.json");

	}
}
