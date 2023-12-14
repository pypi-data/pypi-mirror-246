mod utils;
use utils::{AST, cmd2ast};
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use whiledb::{SrcError, parse as whiledb_parse};


/// Formats the sum of two numbers as string.
#[pyfunction]
fn parse(src: String) -> PyResult<AST> {
    match whiledb_parse(&src) {
        Ok(tree) => {
            Ok(cmd2ast(&tree))
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
