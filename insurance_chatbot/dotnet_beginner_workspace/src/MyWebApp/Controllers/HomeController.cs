using Microsoft.AspNetCore.Mvc;

namespace MyWebApp.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            ViewData["Message"] = "Welcome to MyWebApp MVC!";
            return View();
        }

        public IActionResult About()
        {
            ViewData["Message"] = "About this simple MVC app.";
            return View();
        }
    }
}
