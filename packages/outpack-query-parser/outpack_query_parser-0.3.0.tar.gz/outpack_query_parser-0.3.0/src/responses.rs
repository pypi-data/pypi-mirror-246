use rocket::http::{ContentType, Status};
use rocket::response::Responder;
use rocket::serde::json::{json, Json};
use rocket::serde::{json, Deserialize, Serialize};
use rocket::{Request, Response};
use std::io;
use std::io::ErrorKind;

use crate::hash;

#[derive(Responder)]
#[response(status = 200, content_type = "json")]
pub struct OutpackSuccess<T> {
    inner: Json<SuccessResponse<T>>,
    header: ContentType,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct OutpackError {
    pub error: String,
    pub detail: String,

    #[serde(skip_serializing, skip_deserializing)]
    pub kind: Option<ErrorKind>,
}

impl From<io::Error> for OutpackError {
    fn from(e: io::Error) -> Self {
        OutpackError {
            error: e.kind().to_string(),
            detail: e.to_string(),
            kind: Some(e.kind()),
        }
    }
}

impl From<hash::HashError> for OutpackError {
    fn from(e: hash::HashError) -> Self {
        OutpackError {
            // later this can be sorted out better; for now keep old
            // behaviour
            error: std::io::ErrorKind::InvalidInput.to_string(),
            detail: e.explanation,
            kind: Some(std::io::ErrorKind::InvalidInput),
        }
    }
}

impl From<json::Error<'_>> for OutpackError {
    fn from(e: json::Error) -> Self {
        match e {
            json::Error::Io(err) => OutpackError::from(err),
            json::Error::Parse(_str, err) => OutpackError::from(io::Error::from(err)),
        }
    }
}

impl<'r> Responder<'r, 'static> for OutpackError {
    fn respond_to(self, req: &'r Request<'_>) -> rocket::response::Result<'static> {
        let kind = self.kind;
        let json = FailResponse::from(self);
        let status = match kind {
            Some(ErrorKind::NotFound) => Status::NotFound,
            Some(ErrorKind::InvalidInput) => Status::BadRequest,
            Some(ErrorKind::UnexpectedEof) => Status::BadRequest,
            _ => Status::InternalServerError,
        };
        Response::build_from(json!(json).respond_to(req).unwrap())
            .status(status)
            .header(ContentType::JSON)
            .ok()
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SuccessResponse<T> {
    pub status: String,
    pub data: T,
    pub errors: Option<Vec<OutpackError>>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct FailResponse {
    pub status: String,
    pub data: Option<String>,
    pub errors: Option<Vec<OutpackError>>,
}

impl From<OutpackError> for FailResponse {
    fn from(e: OutpackError) -> Self {
        FailResponse {
            status: String::from("failure"),
            data: None,
            errors: Some(Vec::from([e])),
        }
    }
}

impl<T> From<T> for OutpackSuccess<T> {
    fn from(obj: T) -> Self {
        OutpackSuccess {
            inner: Json(SuccessResponse {
                status: String::from("success"),
                data: obj,
                errors: None,
            }),
            header: ContentType::JSON,
        }
    }
}
