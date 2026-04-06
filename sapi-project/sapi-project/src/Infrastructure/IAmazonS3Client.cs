using System.Threading;
using System.Threading.Tasks;

namespace SapiProject.Infrastructure
{
    public interface IAmazonS3Client
    {
        Task UploadAsync(string bucketName, string keyPath, byte[] content, string? contentType, CancellationToken cancellationToken = default);
    }
}