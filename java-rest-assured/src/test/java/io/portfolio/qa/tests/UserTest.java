package io.portfolio.qa.tests;

import io.portfolio.qa.base.BaseTest;
import io.portfolio.qa.models.Post;
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

@Feature("Users + Posts")
public class UserTest extends BaseTest {

    @Test(groups = {"smoke"})
    @Description("Single user deserializes to our POJO and matches schema")
    public void singleUserMatchesSchemaAndDeserializes() {
        User user = given()
                .spec(jsonplaceholder)
        .when()
                .get("/users/2")
        .then()
                .statusCode(200)
                .time(lessThan(ApiClient.maxResponseMs()))
                .body(SchemaValidator.matchesSchema("single-user.json"))
                .extract()
                .as(User.class);

        org.testng.Assert.assertNotNull(user.getEmail(), "email should deserialize");
        // proves the @JsonProperty("username") -> userName mapping fired
        org.testng.Assert.assertNotNull(user.getUserName(), "username -> userName");
        org.testng.Assert.assertNotNull(user.getCompany().getName(), "nested company");
    }

    @Test(groups = {"smoke"})
    @Description("The user directory holds exactly ten seeded users")
    public void directoryHasTenUsers() {
        given()
                .spec(jsonplaceholder)
        .when()
                .get("/users")
        .then()
                .statusCode(200)
                .body("size()", equalTo(10));
    }

    @DataProvider(name = "pages")
    public Object[][] pages() {
        return new Object[][]{{1}, {2}};
    }

    @Test(groups = {"regression"}, dataProvider = "pages")
    @Description("Post pagination respects the page limit and advertises the total")
    public void postPagination(int page) {
        given()
                .spec(jsonplaceholder)
                .queryParam("_page", page)
                .queryParam("_limit", 10)
        .when()
                .get("/posts")
        .then()
                .statusCode(200)
                // jsonplaceholder reports the full count in a header, not the body
                .header("X-Total-Count", equalTo("100"))
                .body("size()", lessThanOrEqualTo(10));
    }

    @Test(groups = {"regression"})
    @Description("Create post echoes the submitted body and assigns id 101")
    public void createPostEchoesPayload() {
        Post draft = Post.builder()
                .title("Release approved")
                .body("Smoke green, no P1 regressions on the release branch.")
                .userId(7)
                .build();

        given()
                .spec(jsonplaceholder)
                .body(draft)
        .when()
                .post("/posts")
        .then()
                .statusCode(201)
                .body(SchemaValidator.matchesSchema("post-create.json"))
                .body("title", equalTo("Release approved"))
                .body("userId", equalTo(7))
                .body("id", equalTo(101)); // jsonplaceholder always returns 101
    }

    @Test(groups = {"regression"})
    @Description("PUT replaces the post body")
    public void putReplacesPost() {
        Post replacement = Post.builder()
                .title("Full replace")
                .body("Replaced via PUT")
                .userId(1)
                .build();

        String title = given()
                .spec(jsonplaceholder)
                .body(replacement)
        .when()
                .put("/posts/1")
        .then()
                .statusCode(200)
                .extract().path("title");

        assertEquals(title, "Full replace");
    }

    @Test(groups = {"regression"})
    @Description("DELETE returns 200")
    public void deletePostReturns200() {
        given()
                .spec(jsonplaceholder)
        .when()
                .delete("/posts/1")
        .then()
                .statusCode(200);
    }
}
