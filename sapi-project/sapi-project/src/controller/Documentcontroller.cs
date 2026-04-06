using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;
using System.Threading.Tasks;
using SapiProject.Models;
using SapiProject.Services;
using SapiProject.Exceptions;

namespace SapiProject.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DocumentController : ControllerBase
    {
        private readonly IDocumentService _documentService;

        public DocumentController(IDocumentService documentService)
        {
            _documentService = documentService;
        }

        [HttpPost]
        [Route("document")]
        [ProducesResponseType(typeof(UploadDocumentResponseDto), 200)]
        [ProducesResponseType(typeof(ErrorResponseDto), 400)]
        [ProducesResponseType(typeof(ErrorResponseDto), 500)]
        [ProducesResponseType(typeof(ErrorResponseDto), 503)]
        public async Task<ActionResult<UploadDocumentResponseDto>> UploadDocument(
            [FromBody][Required] UploadDocumentRequestDto request)
        {
            try
            {
                var response = await _documentService.UploadDocumentAsync(request);
                return Ok(response);
            }
            catch (ApiException ex)
            {
                var error = new ErrorResponseDto
                {
                    Code = ex.Code,
                    Message = ex.Message,
                    Description = ex.Message,
                    DateTime = System.DateTime.UtcNow,
                    TransactionId = "txn-error"
                };
                return StatusCode(ex.StatusCode, error);
            }
        }
    }
}