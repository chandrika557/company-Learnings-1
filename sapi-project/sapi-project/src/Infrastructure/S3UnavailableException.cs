using System;

namespace SapiProject.Infrastructure
{
    public class S3UnavailableException : Exception
    {
        public S3UnavailableException(string message) : base(message) { }
    }
}