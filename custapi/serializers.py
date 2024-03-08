import json
from urllib import request
from rest_framework import serializers
from .models import * 
from register.models import User
from dashboard.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class CustomerSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    class Meta:
        model = Customer
        fields = ['subscription', 'username', 'email', 'phone']


    
class CustomerCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    password = serializers.CharField(max_length=500, source='user.password')
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True},}


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(
            username = user_data['username'],
            email = user_data['email'],
            phone = user_data['phone'],
            role = User.CUSTOMER,
        )
        user.set_password(user_data['password'])
        user.save()
        customer = Customer.objects.create(user=user)
        return customer

  

class AddressSerializer(serializers.ModelSerializer):
    cust = CustomerSerializer(read_only=True)
    class Meta:
        model = Address
        fields = '__all__'
        # read_only_fields = ['cust']
    def create(self, validated_data):
        customer = Customer.objects.get(user = self.context['request'].user)
        validated_data['cust'] = customer
        return super().create(validated_data)




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


        
class CartSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['restaurant']
    def create(self, validated_data):
        validated_data['customer'] = Customer.objects.get(user_id=self.context['request'].user.id)
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = CustomerSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['author', 'food', 'restaurant', 'order', 'score', 'content', 'answer']



class RAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantAddress
        fields = '__all__'
# ['saturday', 'sunday', 'monday', 'thusday', 'wednesday', 'thursday', 'friday']


class RTiming(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['start', 'end']


class RScheduleSerializer(serializers.ModelSerializer):
    saturday = RTiming()
    sunday = RTiming()
    monday = RTiming()
    thusday = RTiming()
    wednesday = RTiming()
    thursday = RTiming()
    friday = RTiming()
    class Meta:
        model = Schedule
        fields = [ 'saturday', 'sunday', 'monday', 'thusday', 'wednesday', 'thursday', 'friday']



class RestaurantSerializer(serializers.ModelSerializer):
    address = RAddressSerializer(many=True)
    schedule = RScheduleSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'restaurant_type', 'address', 'is_open', 'image', 'average_score', 'comments_count', 'schedule']
        # read_only_fields = ['rating']
# ['id', 'name', 'restaurant_type', 'address_set', 'is_open', 'image', 'average_score', 'comments_count', 'schedules_set']
        


class RestaurantsListSerializer(serializers.ModelSerializer):
    address = RAddressSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'restaurant_type', 'address', 'is_open', 'image', 'average_score']



class FoodSerializer(serializers.ModelSerializer):
    # restaurant = RestaurantSerializer(many=True)
    class Meta:
        model = Food
        fields = ['id', 'name', 'selling_price', 'discount', 'ingredients', 'image']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.discount:
            rep['discount'] = {
                "label": f"{instance.discount}%",
                'factor':  1 - (instance.discount /  100)
                # "factor": int(instance.selling_price) - int(instance.selling_price) * (int(instance.discount) /100)
            }
        return rep

class CategorySerializer(serializers.ModelSerializer):
    category_foods = FoodSerializer(many=True)
    class Meta:
        model = FoodCategory
        fields = ['id', 'FoodCategory', 'category_foods']



class CartRestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','name', 'image']


class ItemSerializer(serializers.ModelSerializer):
    food = serializers.StringRelatedField()
    food_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'food_id', 'food', 'count', 'price']
        read_only_fields = ['price',]



class CartSerializer(serializers.ModelSerializer):
    restaurant = CartRestSerializer()
    foods = ItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'restaurant', 'foods', 'created_at', 'updated_at']


class PaymentSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    cvv = serializers.IntegerField()
    password = serializers.IntegerField()
    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class CommentAuthorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        # this field should be changed to customer
        model = Customer
        fields = ['user']


class OrderComSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['content']
    def get_content(self, obj):
        # Assuming `foods` is a related name for the related model
        # that holds the food names. Adjust this as per your model structure.
        food_names = []
        c = obj.content
        try:
            json_objects = json.loads(c)
            for i in json_objects:
                food_names.append(i['food'])
        except:
            None
        return food_names



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerComment
        fields = ['answer', 'comment']


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer()
    order = OrderComSerializer()
    answer = AnswerSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['author', 'order', 'score', 'content', 'answer', 'created_at']
        read_only_fields = ['author', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            answer = AnswerComment.objects.get(comment=instance)
            representation['answer'] = answer.answer
        except AnswerComment.DoesNotExist:
            if 'answer' in representation:
                del representation['answer']
        return representation



class OrderFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(OrderFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(cus=Customer.objects.get(user_id=self.context['request'].user.id))




class CommentCreateSerializer(serializers.ModelSerializer):
    order = OrderFilteredPrimaryKeyRelatedField(queryset=Order.objects)

    class Meta:
        model = Comment
        fields = ['author', 'restaurant', 'order', 'score', 'content']
        read_only_fields = ['author', 'restaurant', 'created_at']


    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = Customer.objects.get(user_id=self.context['request'].user.id)
        validated_data['restaurant'] = Restaurant.objects.get(id=self.context['pk'])
        return super().create(validated_data)
    



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance:
    #         # If this is an update operation, keep the original queryset.
    #         self.fields['order'].queryset = Order.objects.filter(cus=self.instance.author)
    #         print('keeeee')
    #     elif self.context.get('request') and self.context['request'].user.is_authenticated:
    #         print('okhhhhhh')
    #         # If this is a create operation, filter the queryset based on the current user.
    #         self.fields['order'].queryset = Order.objects.filter(cus=self.context['request'].user)


