# Sinhala Search Engine
A Search Engine API in Sinhala language for famous people in Sri Lankan film industry

## Corpus
Data are scraped from https://www.films.lk

Total records - 500

Structure of a record
```
id
name
real_name
birth
death
bio
films.role
films.title
films.year
awards.title
awards.instituition
```

A Sample Record
```
{
    "id": 0, 
    "name": "රුක්මනී දේවි", 
    "real_name": "ඩේසි රසම්මා ඩැනියල්ස්", 
    "birth": "1923 ජනවාරි 15", 
    "death": "1978 ඔක්තෝම්බර් 28", 
    "bio": "රුක්මනී දේවි යනු ශ්‍රී ලංකාවේ නයිටිංගේල් ලෙස නිතර ප්‍රශංසාවට පාත්‍ර වූ ශ්‍රී ලාංකික ගායිකාවක් සහ නිළියකි...", 
    "films": [
        {
            "title": "කඩවුණු පොරොන්දුව", 
            "role": "ප්‍රධාන නිළිය", 
            "year": "1947"
        }, 
        {
            "title": "කපටි ආරක්ෂකයා", 
            "role": "ප්‍රධාන නිළිය", 
            "year": "1948"
        }, 
        {
            "title": "වැරදුනු කුරුමානම", 
            "role": "ප්‍රධාන නිළිය", 
            "year": "1948"
        },
        ...
    ], 
    "awards": [
        {
            "title": "ජනප්‍රියම නිළිය", 
            "instituition": "දිනමින රඟ මඩල 1956"
        }, 
        {
            "title": "හොඳම නිළිය", 
            "instituition": "1වන දීපෂිකා සම්මාන උළෙල 1956"
        },
        ...
    ]
}

```

## ElasticsSearch

Mapping
```
mapping = {
    "settings" : {
        "analysis" : {
            "analyzer" : {
                "sinhala_analyzer" : {
                    "type": "standard",
                    "stopwords": stopwords
                }
            }
        } 
    },
    "aliases": { 
        "artists": { 
            "is_write_index": True 
        }
    },
    "mappings" : {
        "properties" : {
            "awards" : {
                "properties" : {
                    "instituition" : {
                        "type" : "text",
                        "analyzer" : "sinhala_analyzer",
                        "fields" : {
                            "keyword" : {
                                "type" : "keyword",
                                "ignore_above" : 256
                            }
                        }
                    },
                    "title" : {
                        "type" : "text",
                        "analyzer" : "sinhala_analyzer",
                        "fields" : {
                            "keyword" : {
                                "type" : "keyword",
                                "ignore_above" : 256
                            }
                        }
                    }
                }
            },
            "bio" : {
                "type" : "text",
                "analyzer" : "sinhala_analyzer"
            },
            "birth" : {
                "type" : "text",
                "analyzer" : "sinhala_analyzer",
            },
            "death" : {
                "type" : "text",
                "analyzer" : "sinhala_analyzer",
            },
            "films" : {
                "properties" : {
                    "role" : {
                        "type" : "text",
                        "analyzer" : "sinhala_analyzer",
                        "fields" : {
                            "keyword" : {
                                "type" : "keyword"
                            }
                        }
                    },
                    "title" : {
                        "type" : "text",
                        "analyzer" : "sinhala_analyzer",
                        "fields" : {
                            "keyword" : {
                                "type" : "keyword"
                            }
                        }
                    },
                    "year" : {
                      "type" : "long"
                    }
                }
            },
            "id" : {
                "type" : "long"
            },
            "name" : {
                "type" : "text",
                "analyzer" : "sinhala_analyzer",
                "fields" : {
                    "keyword" : {
                        "type" : "keyword"
                    }
                }
            },
            "real_name" : {
                "type" : "text",
                "analyzer" : "sinhala_analyzer",
                "fields" : {
                    "keyword" : {
                      "type" : "keyword"
                    }
                }
            }
      }
    }
}
```

## Features

1. Keyword Search
   eg :- රුක්මනී දේවි

2. Phrase Search
   eg :- ශ්‍රී ලංකාවේ නයිටිංගේල්

3. Faceted Search
   Can be filtered by
   * Role eg :- නළුවා
   * Movie eg :- කඩවුණු පොරොන්දුව
   * Award eg :- හොඳම රංගනය


4. Wildcard Query
   eg :- විමල* --> විමලධර්ම, විමලසිංහ, විමලරත්න

5. Spell Suggestions
   eg :- රවිනද්‍ර --> රවින්ද්‍ර

## Directory Structure
```
.
├── backend
│   ├── flaskr
│   ├── instance
│   └── venv
├── corpus
├── es
│   └── util
└── frontend
    ├── dist
    └── sources

```