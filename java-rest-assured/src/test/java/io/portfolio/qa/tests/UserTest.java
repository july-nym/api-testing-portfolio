package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.portfolio.qa.models.User;
import io.portfolio.qa.utils.ApiClient;
import io.portfolio.qa.utils.SchemaValidator;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;
import static org.testng.Assert.assertEquals;

@Feature("Users")
public class UserTest extends BaseTest {

    @Test(groups = {"smoke"})
    @Description("Single user response deserializes to our POJO and matches schema")
    public void singleUserMatchesSchemaAndDeserializes() {
        // POJO deserialization proves the @JsonProperty snake_case mapping works
        User user = given()
                .spec(reqres)
        .when()
                .get("/users/2")
        .then()
                .statusCode(200)
                .time(lessThan(ApiClient.maxResponseMs()))
                .body(SchemaValidator.matchesSchema("single-user.json"))
                .extract()
                .jsonPath()
                .getObject("data", User.class);

        org.testng.Assert.assertNotNull(user.getEmail(), "email should deserialize");
        org.testng.Assert.assertNotNull(user.getFirstName(), "first_name -> firstName");
    }

    @DataProvider(name = "pages")
    public Object[][] pages() {
        return new Object[][]{{1}, {2}};
    }

    @Test(groups = {"regression"}, dataProvider = "pages")
    @Description("User list pagination returns the requested page within page size")
    public void userListPagination(int page) {
        given()
                .spec(reqres)
                .queryParam("page", page)
        .when()
                .get("/users")
        .then()
                .statusCode(200)
                .body("page", equalTo(page))
                .body("data.size()", lessThanOrEqualTo(
                        given().spec(reqres).queryParam("page", page)
                                .get("/users").jsonPath().getInt("per_page")));
    }

    @Test(groups = {"regression"})
    @Description("Create user echoes the submitted payload and assigns an id")
    public void createUserEchoesPayload() {
        given()
                .spec(reqres)
                .body("{\"name\":\"Sofia Marchetti\",\"job\":\"QA Lead\"}")
        .when()
                .post("/users")
        .then()
                .statusCode(201)
                .body("name", equalTo("Sofia Marchetti"))
                .body("job", equalTo("QA Lead"))
                .body("id", notNullValue())
                .body("createdAt", notNullValue());
    }

    @Test(groups = {"regression"})
    @Description("PUT replaces the resource and stamps updatedAt")
    public void putReplacesUser() {
        String newJob = given()
                .spec(reqres)
                .body("{\"name\":\"Sofia Marchetti\",\"job\":\"Principal QA\"}")
        .when()
                .put("/users/2")
        .then()
                .statusCode(200)
                .body("updatedAt", notNullValue())
                .extract().path("job");

        assertEquals(newJob, "Principal QA");
    }

    @Test(groups = {"regression"})
    @Description("DELETE returns 204 with no content")
    public void deleteUserReturns204() {
        given()
                .spec(reqres)
        .when()
                .delete("/users/2")
        .then()
                .statusCode(204);
    }
}
