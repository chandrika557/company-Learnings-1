# dotnet_beginner_workspace

This workspace contains a small set of beginner-friendly .NET projects to learn the basics of .NET console apps and ASP.NET Core MVC.

Folders
- `src/MyApp` - Simple console application with a service class and unit tests (already present).
- `src/MyWebApp` - Minimal ASP.NET Core MVC app (controllers + views) created for learning.
- `tests/MyApp.Tests` - Unit tests for `MyService` using xUnit.

How the MVC app is structured (`src/MyWebApp`)
- `Program.cs` - App startup (registers MVC services and routes).
- `MyWebApp.csproj` - Project file targeting .NET 8.0 (`Microsoft.NET.Sdk.Web`).
- `Controllers/HomeController.cs` - Example controller with two actions: `Index` and `About`.
- `Views/Home/Index.cshtml` - Razor view for the `Index` action.
- `Views/Home/About.cshtml` - Razor view for the `About` action.
- `Views/Shared/_Layout.cshtml` - Shared layout used by views.

Run the MVC app
1. Open a terminal in the workspace root:

```powershell
cd "c:\Users\JayaChandrikaEdiga\OneDrive - ValueMomentum, Inc\Documents\insurance_chatbot\dotnet_beginner_workspace\src\MyWebApp"
```

2. Restore and run the app using the `dotnet` CLI:

```powershell
dotnet restore
dotnet run
```

3. By default the app runs on `http://localhost:5000` (and `https://localhost:5001`) — open your browser and navigate to `http://localhost:5000` and try the `Home` and `About` links.

Notes and next steps
- Open the folder in Visual Studio Code or Visual Studio. In VS Code you'll get C# language features if you install the C# extension (OmniSharp).
- To add a solution file and tie projects together:
  ```powershell
  cd dotnet_beginner_workspace
  dotnet new sln -n dotnet_beginner_workspace
  dotnet sln add src/MyApp/MyApp.csproj
  dotnet sln add src/MyWebApp/MyWebApp.csproj
  dotnet sln add tests/MyApp.Tests/MyApp.Tests.csproj
  ```
- Add more controllers, static files under `wwwroot`, or Entity Framework Core for data access as you progress.

If you want, I can:
- Create a solution file and wire both projects and tests into it.
- Add a quick CSS file under `wwwroot/css/site.css` and static assets.
- Add instructions for debugging in VS Code.

---

## MyWebApi (Web API)

This project demonstrates a small Web API built with ASP.NET Core. It uses a simple in-memory repository pattern so you can run and experiment without adding a database.

Files created
- `MyWebApi.csproj` - Project file (net8.0) with Swashbuckle for Swagger UI.
- `Program.cs` - App startup; registers controllers and repository and enables Swagger in Development.
- `Controllers/ProductsController.cs` - Example API controller exposing CRUD endpoints:
  - GET /api/products
  - GET /api/products/{id}
  - POST /api/products
  - PUT /api/products/{id}
  - DELETE /api/products/{id}
- `Models/Product.cs` - Simple POCO product model.
- `Services/IProductRepository.cs` - Repository interface.
- `Services/InMemoryProductRepository.cs` - Thread-safe in-memory implementation.

Run the Web API
1. Open a terminal in the Web API folder:

```powershell
cd "c:\Users\JayaChandrikaEdiga\OneDrive - ValueMomentum, Inc\Documents\insurance_chatbot\dotnet_beginner_workspace\src\MyWebApi"
```

2. Restore and run:

```powershell
dotnet restore
dotnet run
```

3. Swagger UI will be available at `https://localhost:5001/swagger` (or the HTTPS URL printed by `dotnet run`) for interactive testing.

Testing endpoints
- Use `curl`, Postman, or the built-in Swagger UI.

Example curl commands:
```powershell
# Get all
curl https://localhost:5001/api/products -k

# Get id 1
curl https://localhost:5001/api/products/1 -k

# Create
curl -X POST https://localhost:5001/api/products -H "Content-Type: application/json" -d '{"name":"New","description":"New item","price":5.5}' -k

# Update
curl -X PUT https://localhost:5001/api/products/2 -H "Content-Type: application/json" -d '{"name":"Updated","description":"Updated","price":15.0}' -k

# Delete
curl -X DELETE https://localhost:5001/api/products/3 -k
```

Notes
- In production you'd replace the in-memory repository with a database-backed repository (EF Core, Dapper, etc.).
- The sample registers `InMemoryProductRepository` as a singleton for simplicity.

Next steps I can do for you
- Add unit tests for the repository and controller (xUnit + Microsoft.AspNetCore.Mvc.Testing).
- Add a solution file (`.sln`) to group the projects.
- Wire up EF Core and a local SQLite database for persistence.

Which of these would you like next?
