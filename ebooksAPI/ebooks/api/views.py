from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from ebooks.models import Ebook,Review
from ebooks.api.serializers import EbookSerializer,ReviewSerializer
from ebooks.api.permissions import IsAdminUserOrReadOnly,IsReviewerOrReadOnly
from rest_framework.exceptions import ValidationError
from ebooks.api.pagination import SmallSetPagination


class EbookListCreateAPIView(generics.ListCreateAPIView):
	queryset = Ebook.objects.all().order_by("-id")
	serializer_class = EbookSerializer
	permission_classes = [IsAdminUserOrReadOnly]
	pagination_class = SmallSetPagination

class EbookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Ebook.objects.all()
	serializer_class = EbookSerializer

class ReviewCreateAPIView(generics.ListCreateAPIView):

	queryset=Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self,serializer):
		print(self.kwargs)
		ebook_pk = self.kwargs.get("ebook_pk")
		ebook = get_object_or_404(Ebook,pk=ebook_pk)
		review_author = self.request.user 
		serializer.ebook=ebook
		try:
			serializer.save(review_author=review_author)
		except IntegrityError:
			raise ValidationError("You have already reviewed this Ebook")


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [IsReviewerOrReadOnly]
