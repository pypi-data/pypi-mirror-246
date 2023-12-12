{% macro current_catalog() -%}
  {{ return(adapter.dispatch('current_catalog', 'dbt')()) }}
{% endmacro %}

{% macro spark__current_catalog() -%}
  {% call statement('current_catalog', fetch_result=True) %}
      select current_catalog()
  {% endcall %}
  {% do return(load_result('current_catalog').table) %}
{% endmacro %}

{% macro use_catalog(catalog) -%}
  {{ return(adapter.dispatch('use_catalog', 'dbt')(catalog)) }}
{% endmacro %}

{% macro spark__use_catalog(catalog) -%}
  {% call statement() %}
    use {{ adapter.quote(catalog.strip()) }}
  {% endcall %}
{% endmacro %}
