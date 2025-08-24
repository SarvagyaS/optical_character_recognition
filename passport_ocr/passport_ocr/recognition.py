"""Passport recognition: MRZ parsing and field extraction."""
import re
from datetime import datetime
from .utils import load_image, preprocess_image
from .ocr import extract_text


def _parse_mrz(lines):
    res = {}
    if not lines:
        return res

    mrz_lines = [l for l in lines if '<' in l and len(l) >= 30]
    if len(mrz_lines) >= 2:
        l1 = mrz_lines[0].replace(' ', '')
        l2 = mrz_lines[1].replace(' ', '')
        res['mrz_line_1'] = l1
        res['mrz_line_2'] = l2

        try:
            if l1.startswith('P'):
                parts = l1.split('<<')
                surname = parts[0][2:]
                given = parts[1].replace('<', ' ').strip() if len(parts) > 1 else ''
                res['surname'] = surname.replace('<', ' ').strip()
                res['given_name'] = given

            passport_num = l2[0:9].replace('<', '')
            res['passport_num'] = passport_num

            country_code = l2[10:13]
            res['country_code'] = country_code

            dob_raw = l2[13:19]
            try:
                res['dob'] = datetime.strptime(dob_raw, '%y%m%d').strftime('%Y-%m-%d')
            except Exception:
                res['dob'] = ''

            gender = l2[20]
            res['gender'] = 'MALE' if gender == 'M' else ('FEMALE' if gender == 'F' else '')

            doe_raw = l2[21:27]
            try:
                res['doe'] = datetime.strptime(doe_raw, '%y%m%d').strftime('%Y-%m-%d')
            except Exception:
                res['doe'] = ''
        except Exception:
            pass

    return res


def _extract_fields(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = '\n'.join(lines)
    data = {k: '' for k in ['doe','dob','father','given_name','mrz_line_1','old_passport_num','file_num','client_id','place_of_issue','spouse','country_code','address','surname','mrz_line_2','passport_num','doi','old_doi','gender','nationality','place_of_birth','mother','old_place_of_issue','pin']}

    mrz = _parse_mrz(lines)
    data.update(mrz)

    m = re.search(r'Passport\s*No[:\s]*([A-Z0-9<-]{6,9})', joined, re.IGNORECASE)
    if m:
        data['passport_num'] = data.get('passport_num') or m.group(1).replace('-', '').replace(' ', '')

    m = re.search(r'Old\s*Passport\s*No[:\s]*([A-Z0-9-]+)', joined, re.IGNORECASE)
    if m:
        data['old_passport_num'] = m.group(1).strip()

    if not data.get('given_name'):
        m = re.search(r'Given\s*Name[s]?:\s*([A-Z\s]+)', joined, re.IGNORECASE)
        if m:
            data['given_name'] = m.group(1).strip()

    if not data.get('surname'):
        m = re.search(r'Surname[:\s]*([A-Z\s]+)', joined, re.IGNORECASE)
        if m:
            data['surname'] = m.group(1).strip()

    m = re.search(r"Father(?:'s)?\s*Name[:\s]*([A-Z\s]+)", joined, re.IGNORECASE)
    if m:
        data['father'] = m.group(1).strip()
    m = re.search(r"Mother(?:'s)?\s*Name[:\s]*([A-Z\s]+)", joined, re.IGNORECASE)
    if m:
        data['mother'] = m.group(1).strip()

    m = re.search(r'Place\s*of\s*Issue[:\s]*([A-Z0-9,\s-]+)', joined, re.IGNORECASE)
    if m:
        data['place_of_issue'] = m.group(1).strip()

    m = re.search(r'Place\s*of\s*Birth[:\s]*([A-Z0-9,\s-]+)', joined, re.IGNORECASE)
    if m:
        data['place_of_birth'] = m.group(1).strip()

    m = re.search(r'Nationality[:\s]*([A-Z\s]+)', joined, re.IGNORECASE)
    if m:
        data['nationality'] = m.group(1).strip()

    m = re.search(r'PIN[:\s]*(\d{5,6})', joined, re.IGNORECASE)
    if m:
        data['pin'] = m.group(1)

    date_patterns = [r'(\d{4}-\d{2}-\d{2})', r'(\d{2}-\d{2}-\d{4})', r'(\d{2}/\d{2}/\d{4})']
    for name in ['doi', 'old_doi']:
        m = re.search(name.replace('_', ' ') + r'[:\s]*(' + '|'.join(date_patterns) + r')', joined, re.IGNORECASE)
        if m:
            date_str = m.group(1)
            try:
                if '-' in date_str and len(date_str.split('-')[0]) == 4:
                    data[name] = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                elif '-' in date_str:
                    data[name] = datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
                else:
                    data[name] = datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except Exception:
                data[name] = ''

    m = re.search(r'Address[:\s]*([A-Z0-9,\s.-]+)', joined, re.IGNORECASE)
    if m:
        data['address'] = m.group(1).strip()

    m = re.search(r'File\s*No[:\s]*([A-Z0-9-]+)', joined, re.IGNORECASE)
    if m:
        data['file_num'] = m.group(1).strip()
    m = re.search(r'Client\s*ID[:\s]*([A-Za-z0-9_-]+)', joined, re.IGNORECASE)
    if m:
        data['client_id'] = m.group(1).strip()

    if not data.get('pin'):
        m = re.search(r'\b(\d{6})\b', joined)
        if m:
            data['pin'] = m.group(1)

    if data.get('country_code') and not data.get('nationality'):
        cc = data['country_code'].upper()
        if cc == 'IND':
            data['nationality'] = 'INDIAN'

    return data


def recognize_passport(image_path):
    image = load_image(image_path)
    processed_image = preprocess_image(image)

    text1 = extract_text(processed_image)
    text2 = extract_text(image)
    combined_text = '\n'.join([text1, text2])

    data = _extract_fields(combined_text)

    result = {
        'data': data,
        'status_code': 200,
        'message': '',
        'success': True
    }

    return result
