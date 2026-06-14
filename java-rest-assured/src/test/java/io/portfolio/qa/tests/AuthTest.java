package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.notNullValue;

@Feature("Authentication")
public class AuthTest extends BaseTest {

    @Test(groups = {"smoke"})
    @Description("A seeded reqres account receives a token on login")
    public void seededUserCanLogIn() {
        given()
                .spec(reqres)
                .body("{\"email\":\"eve.holt@reqres.in\",\"password\":\"cityslicka\"}")
        .when()
                .post("/login")
        .then()
                .statusCode(200)
                .body("token", notNullValue());
    }

    @Test(groups = {"smoke"})
    @Description("Register returns reqres' fixed id and a token")
    public void registerReturnsIdAndToken() {
        given()
                .spec(reqres)
                .body("{\"email\":\"eve.holt@reqres.in\",\"password\":\"pistol\"}")
        .when()
                .post("/register")
        .then()
                .statusCode(200)
                .body("id", greaterThan(0))
                .body("token", notNullValue());
    }

    @Test(groups = {"smoke", "regression"})
    @Description("restful-booker issues a usable session token")
    public void bookerIssuesToken() {
        // bookerToken() asserts a 200 internally; reaching here means it worked
        String token = bookerToken();
        org.testng.Assert.assertTrue(token != null && token.length() > 10,
                "Expected a non-trivial booker token");
    }
}
