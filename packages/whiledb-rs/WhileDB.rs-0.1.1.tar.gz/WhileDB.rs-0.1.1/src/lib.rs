use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use whiledb;
use whiledb::src_error::SrcError;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn parse(src: String) -> PyResult<String> {
    match whiledb::parse(&src) {
        Ok(tree) => {
            Ok(format!("{:?}", tree))
        },
        Err(err) => {
            let msg = match err {
                SrcError::LexerError(_, msg) => msg,
                SrcError::ParseError(_, msg) => msg,
                SrcError::SelfError(msg) => msg,
                SrcError::SelfWarning(_, msg) => msg,
            };
            Err(PyRuntimeError::new_err(msg))
        },
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn whiledb_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    Ok(())
}
