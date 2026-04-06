You are a senior .NET Core architect/developer.

Convert the following MuleSoft raml flow into an ASP.NET Core Web API implementation.

Guidelines:
- Undrstand current solution Architecture follow and coding standards
- Create appropriate Api Endpoint in Controller
- Create RESTful Controller
- Use async/await operations
- Use newly created Request, Response Model classes
- Include proper HTTP status codes based on mule code


if it `type` is defined with custom type-name, error-type-name, success-example, errors-example and prompt input does not have that definition then ask a question to provide the information before generating the code.
when to ask question:
type: Surety.SuretyBondNumber

when not to ask question:
type: string, integer, boolean, date-only, date-time-only, number, nil

if `type-name` is tied to some response then give response type placeholder value as per naming conventions.
Example: Surety.UnderWriterResponse → UnderwriterInformationResponse

Exclude `error-type-name` from the output


One-shot example:
Mule HTTP Listener → ASP.NET Core Controller
Mule raml Code:
          
/underwriter:
  description: This endpoint gets the bonds information for the Under Writer Screen
  securedBy: jwt
  is:
    - clientIdAndSecret:
  type:
    member:
      type-name: Surety.UnderWriterResponse
      error-type-name: Error
      success-example: !include /exchange_modules/6b76c506-4672-4eaf-baeb-5c68ceb63ac1/surety-library/3.0.21/examples/under-writer/under-writer-response.raml
      errors-example: !include /exchange_modules/6b76c506-4672-4eaf-baeb-5c68ceb63ac1/system-error-data-type/2.0.3/examples/message-response.raml
  get:
    queryParameters:
      bond_number:
        required: true
        type: string 

Expected Output:

Dotnet core Web Api Controller & Endpoint:
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
                SwaggerDefault("HARD-CODED-VALUE")
            ]
            string bondNumber
        )
        {
            return Ok(await underwriterProvider.GetUnderwriterInformation(bondNumber));
        }