import json

table = [{
        'Columns View': 'SO Number',
        'Sort By': '',
        'Highlight By': 'equals=S110=rgba(172,86,86,1)/equals=S111',
        'Condition': 'equals=S110,equals=S111',
        'Row Height': '60',
        'Lines per page': '25'
    },
    {
        'Columns View': 'Client PO',
        'Sort By': '',
        'Highlight By': 'equals=S110,equals=S111',
        'Condition': '',
        'Row Height': '',
        'Lines per page': ''
    },
    {
        'Columns View': 'Terms of Sale',
        'Sort By': 'asc',
        'Highlight By': 'equals=ToS110=rgba(172,86,86,1)',
        'Condition': '',
        'Row Height': '',
        'Lines per page': ''
    }
]

websocket_response = {
    'Client PO': {
        'index': 'so_list_client_po',
        'filter': 'client_po'
    },
    'SO Number': {
        'index': 'so_list_so_number',
        'filter': 'so_no'
    },
    'Terms of Sale': {
        'index': 'so_list_terms_of_sale',
        'filter': 'term_sale'
    }
}

base_ws = {
    'Columns View': 'columns',
    'Sort By': 'order_by',
    'Condition': 'conditions_data',
    'Lines per page': 'page_size',
    'Row Height': 'row_height',
    'Highlight By': 'color_conditions'
}

result = {
    'columns': [{
        'index': 'so_list_so_number',
        'sort': 0
    }, {
        'index': 'so_list_client_po',
        'sort': 1
    }, {
        'index': 'so_list_terms_of_sale',
        'sort': 2
    }],
    'order_by': {
        'direction': 'asc',
        'index': 'so_list_terms_of_sale'
    },
    'conditions_data': {
        'so_no': [{
            'type': 'equals',
            'value': 'S110'
        }, {
            'type': 'equals',
            'value': 'S111'
        }],
        'client_po': [{
            'type': 'equals',
            'value': 'P110'
        }]
    },
    'page_size': '25',
    'row_height': '60',
    'color_conditions': {
        'so_no': [{
            'type': 'equals',
            'value': 'S110',
            'color': 'rgba(172,86,86,1)'
        }],
        'client_po': [{
            'type': 'equals',
            'value': 'S110',
            'color': ''
        }, {
            'type': 'equals',
            'value': 'S111',
            'color': ''
        }],
        'term_sale': [{
            'type': 'equals',
            'value': 'S113',
            'color': ''
        }, {
            'type': 'equals',
            'value': 'S112',
            'color': ''
        }]
    },
    'module': 'SO'
}

def parse_conditions(conditions):
    conditions_list = []
    for condition in conditions.split(','):
        if '=' in condition:
            condition_type, condition_value = condition.split('=')
            conditions_list.append({'type': condition_type, 'value': condition_value})
    return conditions_list

def parse_highlight_by(highlight_by):
    highlight_list = []
    for highlight in highlight_by.split('/'):
        parts = highlight.split('=')
        if len(parts) == 3:
            highlight_type, highlight_value, color = parts
        elif len(parts) == 2:
            highlight_type, highlight_value = parts
            color = ''
        highlight_list.append({'type': highlight_type, 'value': highlight_value, 'color': color})
    return highlight_list

def transform_table_to_json(table, websocket_response, base_ws):
    result = {base_ws['Columns View']: []}
    order_by = {}
    conditions_data = {}
    color_conditions = {}

    for i, row in enumerate(table):
        column_view = row.get('Columns View')
        if column_view in websocket_response:
            column_info = websocket_response[column_view]
            result[base_ws['Columns View']].append({'index': column_info['index'], 'sort': i})
            if row.get('Sort By'):
                order_by = {'direction': row['Sort By'], 'index': column_info['index']}
            if row.get('Condition'):
                conditions = parse_conditions(row['Condition'])
                if column_info['filter'] in conditions_data:
                    conditions_data[column_info['filter']].extend(conditions)
                else:
                    conditions_data[column_info['filter']] = conditions
            if row.get('Highlight By'):
                highlights = parse_highlight_by(row['Highlight By'])
                if column_info['filter'] in color_conditions:
                    color_conditions[column_info['filter']].extend(highlights)
                else:
                    color_conditions[column_info['filter']] = highlights

    result[base_ws['Sort By']] = order_by
    result[base_ws['Condition']] = conditions_data
    result[base_ws['Highlight By']] = color_conditions
    result[base_ws['Row Height']] = table[0].get('Row Height', '')
    result[base_ws['Lines per page']] = table[0].get('Lines per page', '')
    result['module'] = 'SO'  # Добавляем статический ключ

    return json.dumps(result, indent=4)

result = transform_table_to_json(table, websocket_response, base_ws)
print(result)