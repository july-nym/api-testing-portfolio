package io.portfolio.qa.base;

import io.portfolio.qa.utils.ApiClient;
import io.restassured.RestAssured;
import io.restassured.specification.RequestSpecification;
import org.testng.annotations.BeforeClass;

/**
 * Shared setup for every test class.
 *
 * Specs are built once per class rather than per method — they're immutable, so
 * sharing is safe and saves rebuilding the header set on each call. The booker
 * auth token is fetched lazily and cached because not every suite needs it (the
 * jsonplaceholder reads don't), and booker's token is valid for the whole run.
 */
public abstract class BaseTest {

    protected RequestSpecification jsonplaceholder;
    protected RequestSpecification booker;

    private String cachedBookerToken;

    @BeforeClass(alwaysRun = true)
    public void initSpecs() {
        jsonplaceholder = ApiClient.jsonplaceholder();
        booker = ApiClient.booker();
        // Log request + response only when an assertion fails — keeps green runs quiet
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    /** Authenticate against booker once, then reuse the token. */
    protected String bookerToken() {
        if (cachedBookerToken == null) {
            cachedBookerToken = io.restassured.RestAssured
                    .given()
                    .spec(booker)
                    .body("{\"username\":\"admin\",\"password\":\"password123\"}")
                    .when()
                    .post("/auth")
                    .then()
                    .statusCode(200)
                    .extract()
                    .path("token");
        }
        return cachedBookerToken;
    }

    /** booker wants the token as a Cookie on write operations. */
    protected String bookerCookie() {
        return "token=" + bookerToken();
    }
}
