# test_generator_id.py

from datetime import datetime
from reddit_api.tools import GeneratorID

def test_id_number_generator():
    generated_id = GeneratorID.id_number_generator()
    assert isinstance(generated_id, int)

def test_get_date():
    generated_id = GeneratorID.id_number_generator()
    generated_date = GeneratorID.get_date(generated_id)

    current_date = datetime.fromtimestamp(generated_id)
    assert generated_date == current_date

def main():
    test_id_number_generator()
    test_get_date()
    print("All tests passed successfully!")

if __name__ == "__main__":
    main()
