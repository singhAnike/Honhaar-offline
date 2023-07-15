from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length=200)

# Serialization
data = {
    'name': 'John',
    'age': 30,
    'address': '123 Main Street'
}
serializer = PersonSerializer(data=data)
serialized_data = serializer.data
print(serialized_data)  # Output: {'name': 'John', 'age': 30, 'address': '123 Main Street'}

# Deserialization
deserializer = PersonSerializer(data=serialized_data)
deserializer.is_valid(raise_exception=True)
deserialized_object = deserializer.save()
print(deserialized_object.name)     # Output: John
print(deserialized_object.age)      # Output: 30
print(deserialized_object.address)  # Output: 123 Main Street
