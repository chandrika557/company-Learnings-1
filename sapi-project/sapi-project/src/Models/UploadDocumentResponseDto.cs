namespace SapiProject.Models
{
    public class UploadDocumentResponseDto
    {
        public string? Code { get; set; }
        public string? Message { get; set; }
        public string? Description { get; set; }
        public DateTime? DateTime { get; set; }
        public string? TransactionId { get; set; }
    }
}