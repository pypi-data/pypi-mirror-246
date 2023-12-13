class JsonErrorParser():
  def is_error_found(self, response):
    if (response.text.split(',')[0].todigit()):
      return response.text.split(',')[0].todigit()
    json = response.json()
    if isinstance(json, list):
      return False
    return json['errorCode']
