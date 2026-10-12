pub fn tokenise(text: &str) -> Vec<String> {
    text.to_lowercase()
        .split(|c: char| !c.is_alphanumeric())
        .filter(|s| !s.is_empty())
        .map(|s| s.to_string())
        .collect()
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn operating_profit_rose() {
        let text = "Operating profit rose".to_string();
        let tokenised = tokenise(&text);
        assert_eq!(tokenised, ["operating", "profit", "rose"]);
    }

    #[test]
    fn sales_fell_costs_rose() {
        let text = "Sales fell , and costs rose .".to_string();
        let tokenised = tokenise(&text);
        assert_eq!(tokenised, ["sales", "fell", "and", "costs", "rose"]);
    }

    #[test]
    fn nada() {
        let text = "".to_string();
        let tokenised = tokenise(&text);
        assert!(tokenised.is_empty())
    }

    #[test]
    fn rose_to_thirteen_point_one() {
        let text = "rose to EUR 13.1m".to_string();
        let tokenised = tokenise(&text);
        assert_eq!(tokenised, ["rose", "to", "eur", "13", "1m"]);
    }
}
