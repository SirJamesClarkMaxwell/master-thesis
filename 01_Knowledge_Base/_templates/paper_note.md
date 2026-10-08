---
citekey: "{{ citekey or citationKey }}"
title: "{{ title | escape }}"
year: "{% if date %}{{ date | format('YYYY') }}{% endif %}"
doi: "{{ DOI or doi }}"
url: "{{ url }}"
zotero_pdf: "{% if pdfZoteroLink %}{{ pdfZoteroLink }}{% endif %}"
tags: []
---

{% macro renderAnnotations(items, calloutType, icon, heading) %}
{%- if items.length > 0 %}

### {{ icon }} {{ heading }}
{%- for annotation in items %}
{%- if annotation.annotatedText or annotation.imageRelativePath or annotation.comment %}

> [!{{ calloutType }}] {{ icon }} {% if annotation.desktopURI %}{% if annotation.pageLabel %}[s. {{ annotation.pageLabel }}]({{ annotation.desktopURI }}){% elif annotation.page %}[s. {{ annotation.page }}]({{ annotation.desktopURI }}){% else %}[Otwórz w Zotero]({{ annotation.desktopURI }}){% endif %}{% elif annotation.pageLabel %}s. {{ annotation.pageLabel }}{% elif annotation.page %}s. {{ annotation.page }}{% endif %}
{% if annotation.annotatedText -%}
> {{ annotation.annotatedText | replace("\n", "\n> ") }}
{% endif -%}
{% if annotation.imageRelativePath -%}
> ![[{{ annotation.imageRelativePath }}|700]]
{% endif -%}
{% if annotation.comment -%}
>
> **Mój komentarz:** {{ annotation.comment | replace("\n", "\n> ") }}
{% endif %}
{% if annotation.id %}
^zot-{{ annotation.id }}
{% endif %}
{%- endif %}
{%- endfor %}
{%- endif %}
{%- endmacro %}

{%- set yellowAnnotations = annotations | filterby("colorCategory", "contains", "Yellow") -%}
{%- set greenAnnotations = annotations | filterby("colorCategory", "contains", "Green") -%}
{%- set blueAnnotations = annotations | filterby("colorCategory", "contains", "Blue") -%}
{%- set purpleAnnotations = annotations | filterby("colorCategory", "contains", "Purple") -%}
{%- set orangeAnnotations = annotations | filterby("colorCategory", "contains", "Orange") -%}
{%- set redAnnotations = annotations | filterby("colorCategory", "contains", "Red") -%}
{%- set grayAnnotations = annotations | filterby("colorCategory", "contains", "Gray") %}

# {{ title | escape }}

## Moje przemyślenia i streszczenie

{% persist "my-notes" %}{% endpersist %}

## Czego chcę od tej pracy

{% persist "what-i-want" %}{% endpersist %}

## Zaznaczenia z Zotero
{{ renderAnnotations(yellowAnnotations, "question", "🟡", "Definicje i fundamenty") }}{{ renderAnnotations(greenAnnotations, "success", "🟢", "Wyniki, liczby i wartości") }}{{ renderAnnotations(blueAnnotations, "info", "🔵", "Mechanizmy i interpretacje") }}{{ renderAnnotations(purpleAnnotations, "example", "🟣", "Idee, powiązania i luki") }}{{ renderAnnotations(orangeAnnotations, "warning", "🟠", "Tło, technologia i materiał do doczytania") }}{{ renderAnnotations(redAnnotations, "danger", "🔴", "Problemy, niejasności i sprzeczności") }}{{ renderAnnotations(grayAnnotations, "quote", "⚪", "Cytaty do potencjalnego wykorzystania") }}
{% if relations and relations.length > 0 %}
## Powiązane publikacje
{%- for related in relations %}
{%- set relatedKey = related.citekey or related.citationKey %}
{%- if relatedKey %}
- [[02_Papers/{{ relatedKey }}|{{ related.title | escape }}]]
{%- endif %}
{%- endfor %}
{% endif %}
