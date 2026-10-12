use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use serde::Deserialize;

#[derive(Debug, Copy, Clone, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Label {
    Negative,
    Neutral,
    Positive,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct Record {
    pub text: String,
    pub label: Label,
}

pub fn read_jsonl(path: &Path) -> Result<Vec<Record>, Box<dyn Error>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut records = Vec::new();

    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let record = serde_json::from_str::<Record>(&line)?;
        records.push(record);
    }

    Ok(records)
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn positive_is_positive() {
        let label = Label::Positive;
        assert_eq!(label, Label::Positive);
    }

    #[test]
    fn positive_isnt_negative() {
        let label = Label::Positive;
        assert_ne!(label, Label::Negative);
    }

    #[test]
    fn seal_is_positive() {
        let record = Record {
            text: "seal".to_string(),
            label: Label::Positive,
        };
        assert_eq!(record.text, "seal");
        assert_eq!(record.label, Label::Positive);
        assert_ne!(record.label, Label::Negative)
    }

    #[test]
    fn sea_lion_is_negative() {
        let record = Record {
            text: "sea lion".to_string(),
            label: Label::Negative,
        };
        assert_eq!(record.text, "sea lion");
        assert_eq!(record.label, Label::Negative);
        assert_ne!(record.label, Label::Positive);
    }

    #[test]
    fn text_is_neutral() {
        let line = r#"{"text": "According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing .", "label": "neutral"}"#;
        let record = serde_json::from_str::<Record>(line);
        assert_eq!(record.unwrap().label, Label::Neutral);
    }

    #[test]
    fn bad_label() {
        let line = r#"{"text": "According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing .", "label": "yippee-ki-yay"}"#;
        let record = serde_json::from_str::<Record>(line);
        assert!(record.is_err());
    }

    #[test]
    fn we_have_records() {
        let records = read_jsonl(Path::new("../../data/jsonl/Sentences_50Agree.jsonl")).unwrap();
        assert!(records.len() > 0);
    }
}
