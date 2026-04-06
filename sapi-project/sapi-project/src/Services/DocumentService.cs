using System;
using System.Threading;
using System.Threading.Tasks;
using SapiProject.Models;
using SapiProject.Infrastructure;
using SapiProject.Exceptions;

namespace SapiProject.Services
{
    public class DocumentService : IDocumentService
    {
        private readonly IAmazonS3Client _s3Client;
        private readonly ITransactionIdProvider _transactionIdProvider;

        public DocumentService(IAmazonS3Client s3Client, ITransactionIdProvider transactionIdProvider)
        {
            _s3Client = s3Client;
            _transactionIdProvider = transactionIdProvider;
        }

        public async Task<UploadDocumentResponseDto> UploadDocumentAsync(UploadDocumentRequestDto request, CancellationToken cancellationToken = default)
        {
            byte[] documentBytes;
            try
            {
                documentBytes = Convert.FromBase64String(request.Document ?? string.Empty);
            }
            catch (FormatException)
            {
                throw new ApiException("Invalid Base64 document", "400", 400);
            }

            var keyPath = $"uploads/{request.FileName}";
            var bucketName = "your-bucket-name"; // Replace with config or logic

            try
            {
                await _s3Client.UploadAsync(bucketName, keyPath, documentBytes, request.ContentType, cancellationToken);
            }
            catch (S3UnavailableException)
            {
                throw new ApiException("S3 Service Unavailable", "503", 503);
            }
            catch (Exception)
            {
                throw new ApiException("Internal Server Error", "500", 500);
            }

            return new UploadDocumentResponseDto
            {
                Code = "200",
                Message = "Success",
                Description = "Document uploaded successfully.",
                DateTime = DateTime.UtcNow,
                TransactionId = _transactionIdProvider.GetTransactionId()
            };
        }
    }
}