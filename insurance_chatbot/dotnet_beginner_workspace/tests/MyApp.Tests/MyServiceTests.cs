using Xunit;
using MyApp;

namespace MyApp.Tests
{
    public class MyServiceTests
    {
        [Fact]
        public void GetGreeting_ReturnsDefault_WhenNameIsNullOrEmpty()
        {
            var service = new MyService();
            var result = service.GetGreeting(null);
            Assert.Contains("Hello", result);
        }

        [Fact]
        public void GetGreeting_IncludesName()
        {
            var service = new MyService();
            var result = service.GetGreeting("Alice");
            Assert.Contains("Alice", result);
        }
    }
}
