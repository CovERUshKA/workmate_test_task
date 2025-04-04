from main import check_files, process_line, process_files


def test_check_files():
    assert check_files(['logs/app1.log'])
    assert check_files(['logs/app1.log', 'logs/app2.log', 'logs/app3.log'])
    assert check_files([]) == False
    assert check_files(['logs/app1.txt', 'logs/app2.log', 'logs/app3.log']) == False
    assert check_files(['logs/app1.txt', 'logs/app2.log', 'logs/app3.log', 'logs/app4.log']) == False
    assert check_files(['logs/app1.txt', 'logs/app2.log', 'logs/app3.log', 'logs/app4']) == False
    assert check_files(['logs/app1.txt', 'logs/app2.log', 'logs/app3.log', 'logs.txt']) == False


def test_process_line():
    line_1 = '2025-03-28 12:04:09,000 INFO django.request: GET /api/v1/products/ 204 OK [192.168.1.44]'
    line_2 = '2025-03-28 12:04:09,000 CRITICAL django.jump: GET /api/v1/products/ 204 OK [192.168.1.44]'
    line_3 = '2025-03-28 12:04:09,000 Bombo django.jump: GET /api/v1/products/ 204 OK [192.168.1.44]'
    line_4 = '2025-03-28 12:04:09,000 INFO'

    assert process_line(line_1) == ("django.request", "INFO")
    assert process_line(line_2) == ("django.jump", "CRITICAL")
    assert process_line(line_3) == False
    assert process_line(line_4) == False
    assert process_line('') == False


def test_process_files():
    files = ['logs/app1.log', 'logs/app2.log', 'logs/app3.log']
    handlers = {}
    total_count = process_files(files, handlers)
    assert len(handlers) == 4
    assert total_count == 300

    files = []
    handlers = {}
    total_count = process_files(files, handlers)
    assert len(handlers) == 0
    assert total_count == 0

    files = ['logs/app1.log', 'logs/app2.log', 'logs/app3.log', 'logs/unknown.log']
    handlers = {}
    total_count = process_files(files, handlers)
    assert len(handlers) == 0
    assert total_count == 0
