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

    @Test(groups = {"negative", "regression"})
    @Description("Login without a password is a 400 with a descriptive error")
    public void loginWithoutPasswordIs400() {
        given()
                .spec(reqres)
                .body("{\"email\":\"peter.holt@reqres.in\"}")
        .when()
                .post("/login")
        .then()
                .statusCode(400)
                .body("error", equalTo("Missing password"));
    }

    @DataProvider(name = "missingIds")
    public Object[][] missingIds() {
        return new Object[][]{{0}, {23}, {999}};
    }

    @Test(groups = {"negative", "regression"}, dataProvider = "missingIds")
    @Description("Unknown reqres user ids return 404")
    public void unknownUserReturns404(int id) {
        given()
                .spec(reqres)
        .when()
                .get("/users/" + id)
        .then()
                .statusCode(404);
    }

    @Test(groups = {"negative", "regression"})
    @Description("A write to booker without the auth cookie is forbidden (403)")
    public void writeWithoutAuthIsForbidden() {
        int bookingId = given().spec(booker)
                .body("{\"firstname\":\"Temp\",\"lastname\":\"Record\",\"totalprice\":1," +
                        "\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"2026-01-01\"," +
                        "\"checkout\":\"2026-01-02\"}}")
                .when().post("/booking")
                .then().statusCode(200).extract().path("bookingid");

        given()
                .spec(booker) // deliberately no Cookie header
                .body("{\"firstname\":\"Temp\",\"lastname\":\"Record\",\"totalprice\":1," +
                        "\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"2026-01-01\"," +
                        "\"checkout\":\"2026-01-02\"}}")
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
