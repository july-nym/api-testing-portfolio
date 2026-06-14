package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

@Feature("Negative cases")
public class NegativeTest extends BaseTest {

    @DataProvider(name = "missingIds")
    public Object[][] missingIds() {
        // jsonplaceholder only seeds 10 users; anything beyond is a 404
        return new Object[][]{{11}, {99}, {999}};
    }

    @Test(groups = {"negative", "regression"}, dataProvider = "missingIds")
    @Description("Unknown user ids return 404")
    public void unknownUserReturns404(int id) {
        given()
                .spec(jsonplaceholder)
        .when()
                .get("/users/" + id)
        .then()
                .statusCode(404);
    }

    @Test(groups = {"negative", "regression"})
    @Description("Unknown post returns 404")
    public void unknownPostReturns404() {
        given()
                .spec(jsonplaceholder)
        .when()
                .get("/posts/9999")
        .then()
                .statusCode(404);
    }

    @Test(groups = {"negative", "regression"})
    @Description("A write to booker without the auth cookie is forbidden (403)")
    public void writeWithoutAuthIsForbidden() {
        String body = "{\"firstname\":\"Temp\",\"lastname\":\"Record\",\"totalprice\":1," +
                "\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"2026-01-01\"," +
                "\"checkout\":\"2026-01-02\"}}";

        int bookingId = given().spec(booker).body(body)
                .when().post("/booking")
                .then().statusCode(200).extract().path("bookingid");

        given()
                .spec(booker) // deliberately no Cookie header
                .body(body)
        .when()
                .put("/booking/" + bookingId)
        .then()
                .statusCode(403);
    }

    @Test(groups = {"negative"})
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
