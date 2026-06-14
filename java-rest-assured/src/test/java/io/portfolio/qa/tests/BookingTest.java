package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.portfolio.qa.models.Booking;
import io.portfolio.qa.utils.SchemaValidator;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;
import static org.testng.Assert.assertEquals;

@Feature("Bookings")
public class BookingTest extends BaseTest {

    private Booking sampleBooking() {
        return Booking.builder()
                .firstname("Mariana")
                .lastname("Okafor")
                .totalprice(845)
                .depositpaid(true)
                .bookingdates(Booking.BookingDates.builder()
                        .checkin("2026-09-12")
                        .checkout("2026-09-19")
                        .build())
                .additionalneeds("Late checkout")
                .build();
    }

    @Test(groups = {"smoke"})
    @Description("Creating a booking returns an id and a schema-valid body")
    public void createBookingReturnsId() {
        given()
                .spec(booker)
                .body(sampleBooking())
        .when()
                .post("/booking")
        .then()
                .statusCode(200)
                .body(SchemaValidator.matchesSchema("booking-create.json"))
                .body("bookingid", notNullValue())
                .body("booking.firstname", equalTo("Mariana"));
    }

    @Test(groups = {"regression"})
    @Description("Full lifecycle: create, read, update with auth, delete, confirm 404")
    public void fullBookingLifecycle() {
        // create
        int bookingId = given()
                .spec(booker)
                .body(sampleBooking())
        .when()
                .post("/booking")
        .then()
                .statusCode(200)
                .extract().path("bookingid");

        // read it back
        given().spec(booker)
        .when().get("/booking/" + bookingId)
        .then().statusCode(200).body("lastname", equalTo("Okafor"));

        // full update needs the auth cookie
        Booking updated = sampleBooking();
        updated.setTotalprice(1290);
        updated.setDepositpaid(false);

        int updatedPrice = given()
                .spec(booker)
                .header("Cookie", bookerCookie())
                .body(updated)
        .when()
                .put("/booking/" + bookingId)
        .then()
                .statusCode(200)
                .extract().path("totalprice");
        assertEquals(updatedPrice, 1290);

        // delete (booker answers 201) then confirm it's gone
        given().spec(booker).header("Cookie", bookerCookie())
        .when().delete("/booking/" + bookingId)
        .then().statusCode(201);

        given().spec(booker)
        .when().get("/booking/" + bookingId)
        .then().statusCode(404);
    }

    @Test(groups = {"regression"})
    @Description("PATCH updates only the targeted field, leaving others intact")
    public void partialUpdateLeavesOtherFields() {
        int bookingId = given().spec(booker).body(sampleBooking())
                .when().post("/booking")
                .then().statusCode(200).extract().path("bookingid");

        given()
                .spec(booker)
                .header("Cookie", bookerCookie())
                .body("{\"additionalneeds\":\"Airport transfer\"}")
        .when()
                .patch("/booking/" + bookingId)
        .then()
                .statusCode(200)
                .body("additionalneeds", equalTo("Airport transfer"))
                .body("firstname", equalTo("Mariana"));
    }
}
