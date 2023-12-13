class JsonErrorParser():
  def is_error_found(self, response):
    print('==============================')
    print(response.url)
    json = response.json()
    print(json)
    if isinstance(json, list):
      return False
    return json['errorCode']
