using System.Threading;
using System.Threading.Tasks;
using SapiProject.Models;

namespace SapiProject.Services
{
    public interface IDocumentService
    {
        Task<UploadDocumentResponseDto> UploadDocumentAsync(UploadDocumentRequestDto request, CancellationToken cancellationToken = default);
    }
}