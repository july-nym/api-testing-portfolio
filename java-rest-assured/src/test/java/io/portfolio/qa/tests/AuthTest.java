package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

@Feature("Authentication")
public class AuthTest extends BaseTest {

    @Test(groups = {"smoke", "regression"})
    @Description("restful-booker issues a usable session token")
    public void bookerIssuesToken() {
        // bookerToken() asserts a 200 internally; reaching here means it worked
        String token = bookerToken();
        org.testng.Assert.assertTrue(token != null && token.length() > 10,
                "Expected a non-trivial booker token");
    }

    @Test(groups = {"negative", "regression"})
    @Description("Bad booker credentials return a reason body rather than a 401")
    public void badCredentialsReturnReason() {
        given()
                .spec(booker)
                .body("{\"username\":\"admin\",\"password\":\"nope\"}")
        .when()
                .post("/auth")
        .then()
                .statusCode(200)
                .body("reason", equalTo("Bad credentials"));
    }
}
