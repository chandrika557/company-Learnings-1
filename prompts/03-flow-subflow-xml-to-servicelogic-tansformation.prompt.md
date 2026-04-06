You are a senior .NET Core architect/developer.

Convert the following MuleSoft flow into an ASP.NET Core Web API implementation.

Guidelines:
- No controller code is needed
- `Do not create additional class for response model`
- Extract business logic into a Service class
- Use async/await methods
- Use newly created Request, Response, Transformation Model Classes
- Include proper HTTP status codes based on mule code
- Include the necessary changes in ApiConfig, BootStrapper files

Input:
- MuleSoft Flow XML
- DWL Transformation Code

Output:
- Service Layer Interface and Implementation 
- C# Mapped for DWL Transformation
- Changes needed in ApiConfig Wrapper class
- Changes needed in BootStrapper to register the new service
============================


One-shot example:
Mule Flow Logic → Service method
Mule XML:
	<sub-flow name="underwriter-main" doc:id="e0df123f-cbb0-404c-bf5e-cd354385fce9" >
		<flow-ref doc:name="common-preserve-attributes" doc:id="a4cc2927-7a48-4a94-9623-995902aabcbe" name="common-preserve-attributes"/>
		<flow-ref doc:name="common-decode-jwt" doc:id="abf78680-064e-4465-9d41-dcdaf8e65829" name="common-decode-jwt"/>
		<ee:transform doc:name='set "bond_number" var without first char' doc:id="a043b763-96b2-4cd2-873c-7a656682fdf4" >
			<ee:variables >
				<ee:set-variable resource="dw/underwriter/set-bond_number-var.dwl" variableName="bond_number" />
			</ee:variables>
		</ee:transform>
		<flow-ref doc:name="underwriter-get-underwriter-info-from-sapi-W-or-5" doc:id="582a0885-dbbb-4c06-aa62-9eeb6510b8c0" name="underwriter-get-underwriter-info-from-sapi-W-or-5"/>

		<set-variable value="#[vars.underwriter_response.agency_number]" doc:name="validAgencyCode" doc:id="238b4cd6-d57e-42ce-bd4b-4daf5e03bb1e" variableName="validAgencyCode"/>
		<flow-ref doc:name="common-verify-agency-access" doc:id="b589c428-fc72-4e12-90ee-0512a8352bfb" name="common-verify-agency-access"/>
		<http:request method="GET" doc:name="GET: surety-bond-sapi/inquiry" doc:id="ed4b1bc6-97a6-4032-93ba-f1eaaa762360" config-ref="Surety_Bond_SAPI_HTTP_Request_configuration" path="/inquiry" target="inquiry_response" >
			<http:headers ><![CDATA[#[output application/java
---
{
	Authorization : vars.request_attributes.headers.Authorization,
	client_secret : vars.request_attributes.headers.client_secret,
	client_id : vars.request_attributes.headers.client_id
}]]]></http:headers>
			<http:query-params ><![CDATA[#[output application/java
---
{
	bond_number : vars.bond_number
}]]]></http:query-params>
		</http:request>
		<ee:transform doc:name="Under Writer Final Response" doc:id="1eed11e4-03ac-4ffd-beba-75ddb54e285b">
			<ee:message>
				<ee:set-payload resource="dw/underwriter/map-final-response.dwl" />
			</ee:message>
		</ee:transform>
	</sub-flow>
	<sub-flow name="underwriter-get-underwriter-info-from-sapi-W-or-5" doc:id="4a8f5b9c-d8d9-4e04-b6a8-e3de996f45f1" >
		<scatter-gather doc:name="get underwriter data using W or 5" doc:id="97863bf3-50b5-475e-b134-8a5dae0157f5" >
			<route >
				<try doc:name="Try" doc:id="b3c47e21-f682-4aeb-b330-252e4412a94c" >
					<set-variable value='#["W" ++ (vars.bond_number default "" as String)]' doc:name="Re set bond_number with W" doc:id="835374e3-9948-4b4c-b772-632a23b6b24a" variableName="bond_number"/>
					<http:request method="GET" doc:name='GET-Surety-Bond-SAPI/under-writer with "W"' doc:id="c0318984-66cd-4963-b20c-ac230b051ede" config-ref="Surety_Bond_SAPI_HTTP_Request_configuration" path="/under-writer" target="underwriter_response">
			<http:headers><![CDATA[#[output application/java
---
{
	Authorization : vars.request_attributes.headers.Authorization,
	client_secret : vars.request_attributes.headers.client_secret,
	client_id : vars.request_attributes.headers.client_id
}]]]></http:headers>
			<http:query-params><![CDATA[#[output application/java
---
{
	bond_number : vars.bond_number,
	request_type: 'C'
}]]]></http:query-params>
		</http:request>
					<error-handler >
						<on-error-propagate enableNotifications="true" logException="true" doc:name="On Error Propagate" doc:id="10f55b2c-8965-4d39-ad11-0065545cbc5c" type="HTTP:UNAUTHORIZED">
							<logger level="ERROR" doc:name="Catching Unauthorized Error" doc:id="c9e02578-12bd-4e63-97b0-d08ca2313c89" />
						</on-error-propagate>
						<on-error-continue enableNotifications="false" logException="false" doc:name="On Error Continue" doc:id="7153bf52-cd2d-410b-8093-60e249ebc6aa" >
							<remove-variable doc:name="bond_number with W" doc:id="ea9d34b6-9384-4d65-931c-2f5c4e174e06" variableName="bond_number"/>

						</on-error-continue>
					</error-handler>
				</try>
			</route>
			<route >
				<try doc:name="Try" doc:id="7157c9f1-7b33-4c51-ae54-61a86bff1237" >
					<set-variable value='#["5" ++ (vars.bond_number default "" as String)]' doc:name='Re set bond_number with "5"' doc:id="8a2d9024-4f92-4ef7-8117-7e07f3bb6ba2" variableName="bond_number"/>
					<http:request method="GET" doc:name='GET-Surety-Bond-SAPI/under-writer with "5"' doc:id="0f840f1c-5e22-4afe-b856-81d7a91be006" config-ref="Surety_Bond_SAPI_HTTP_Request_configuration" path="/under-writer" target="underwriter_response">
			<http:headers><![CDATA[#[output application/java
---
{
	Authorization : vars.request_attributes.headers.Authorization,
	client_secret : vars.request_attributes.headers.client_secret,
	client_id : vars.request_attributes.headers.client_id
}]]]></http:headers>
			<http:query-params><![CDATA[#[output application/java
---
{
	bond_number : vars.bond_number,
	request_type: 'C'
}]]]></http:query-params>
		</http:request>
				<error-handler >
						<on-error-propagate enableNotifications="true" logException="true" doc:name="On Error Propagate" doc:id="f7a34ed1-86a5-48ae-aafc-fc65f8db7a80" type="HTTP:UNAUTHORIZED">
							<logger level="ERROR" doc:name="Catching Unauthorized Error" doc:id="1272dae8-fb8d-4fc5-9dec-4c1f99971d3d" />
						</on-error-propagate>
						<on-error-continue enableNotifications="false" logException="false" doc:name="On Error Continue" doc:id="22e6f8a8-d603-4713-9879-2649ceb96c9d" >
							<remove-variable doc:name="bond_number with 5" doc:id="95f885a8-5f71-4ef7-9805-4894298873b3" variableName="bond_number"/>

						</on-error-continue>
					</error-handler>
				</try>
			</route>
		</scatter-gather>
	</sub-flow>
===========================
DWL Input:
%dw 2.0
output application/json skipNullOn = "everywhere"
{
	account_number: uwresponse.account_number,
	bond_type: uwresponse.bond_type,
    bond_status: uwresponse.bond_status
}
=============================
Expected Output:
  Service Layer:
  Interface Implementation:
  public interface IUnderwriterProvider
  {
    Task<UnderwriterInformationResponse> GetUnderwriterInformation(string bondNumber);
  }

  Class Implementation:
  public class UnderwriterProvider(ApiConfigWrapper apiConfig, IBondProvider bondProvider) : IUnderwriterProvider
  {
      public async Task<UnderwriterInformationResponse> GetUnderwriterInformation(string bondNumber)
        {
            var jwtSecurityToken = JwtClaims.Parse(apiConfig.RequestAuthorization);

            var underwriterResponse = await GetUnderwriterInfoParallel(bondNumber);

            var validAgencyCode = underwriterResponse.AgencyNumber;
            Common.VerifyAgencyAccess(jwtSecurityToken, validAgencyCode);

            var inquiryResponse = await GetInquiryData(bondNumber);

            return MapToUnderwriterInformationResponse(underwriterResponse, inquiryResponse);
        }

      private async Task<UnderWriterResponse> GetUnderwriterInfoParallel(string bondNumber)
        {
            var bondNumberWithoutPrefix = bondNumber.Length > 1 ? bondNumber[1..] : bondNumber;

            var bondNumberWithW = $"W{bondNumberWithoutPrefix}";
            var bondNumberWith5 = $"5{bondNumberWithoutPrefix}";

            var taskW = GetUnderwriterInfoWithPrefixResponse(bondNumberWithW);
            var task5 = GetUnderwriterInfoWithPrefixResponse(bondNumberWith5);

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

    private async Task<UnderWriterResponse?> GetUnderwriterInfoWithPrefixResponse(string bondNumberPrefix)
    {
        using var suretySystemClient = apiConfig.GetSuretySystemClient();
        try
        {
            var response = await suretySystemClient.GetAsync<UnderWriterResponse>(
                $"under-writer?bond_number={bondNumberPrefix}&request_type=C",
                useSnakeCase: true
            );
            return response;
        }
        catch (HttpResponseException ex) when (ex.Response.StatusCode == HttpStatusCode.Unauthorized)
        {
            throw;
        }
        catch (HttpResponseException)
        {
            return null;
        }
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
            
            AccountNumber = underwriterResponse?.AccountNumber,
            BondType = underwriterResponse?.BondType,
            BondStatus = bondStatus
        };
    }
}

===========================

ApiConfigWrapper file changes:
.....

public class ApiConfigWrapper(IOptions<SuretyPAPIConfig> SuretyPAPIConfig, IHttpContextAccessor httpContextAccessor)
{
	public virtual required SuretyPAPIConfig Config { get; set; } = SuretyPAPIConfig.Value;
	public virtual string? RequestAuthorization => httpContextAccessor?.HttpContext?.Request.Headers.Authorization;
}

==============================
Bootstrapper changes:

public void Bootstrap(WebApplicationBuilder builder)
{
   builder.Services.AddTransient<IUnderwriterProvider, UnderwriterProvider>();
}
			