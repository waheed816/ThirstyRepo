import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { thunkCreateProductReview } from '../../store/reviews';
import { useModal } from "../../context/Modal";
import './CreateNewReview.css';

const CreateNewReview = (product) => {
  const product_id = parseInt(product.product);
  const dispatch = useDispatch();
  const [review, setReview] = useState("");
  const [cups, setCups] = useState(1);
  const [reviewButton, setReviewButton] = useState();
  const [hoveredCups, setHoveredCups] = useState(1);
  const [errors, setErrors] = useState('');
  const numbers = [1, 2, 3, 4, 5];
  const { closeModal } = useModal();

  const handleSubmit = (e) => {
    e.preventDefault();

    let allErrors = {}

    if (review.length < 3 || review.length > 255) allErrors.review = 'Review must be between 3 and 255 characters'

    if (Object.keys(allErrors).length) {
      return setErrors(allErrors)
    }

    const newReview = {
      review,
      rating: cups
    };

    dispatch(thunkCreateProductReview(product_id, newReview));
    closeModal();
  };

  const handleMouseOver = (num) => {
    setHoveredCups(num);
  };

  const handleMouseLeave = () => {
    setHoveredCups(null);
  };

  const changeClassName = (value) => {
    if (hoveredCups !== null) {
      return value <= hoveredCups
        ? "fa-solid fa-wine-glass"
        : "fa-solid fa-wine-glass-empty";
    }
    if (value <= cups) {
      return "fa-solid fa-wine-glass";
    }
    return "fa-solid fa-wine-glass-empty";
  };

  const disabledButton = () => {
    if (!cups) return true;
    return false;
  };

  useEffect(() => {
    if (!cups || review.length < 3) {
      setReviewButton("review-button-disabled");
    } else {
      setReviewButton("review-button-enabled");
    }
  }, [cups, review]);

  return (
    <div className="new-review-container">
      <h2 className="title-header">Leave Your Review</h2>
      <form onSubmit={handleSubmit} className="review-form">
        {errors.review ? <p className='new-review-errors'>{errors.review}</p> : null}
        <textarea
          className="review-text-box"
          type="text"
          rows="10"
          value={review}
          placeholder="Leave your review here"
          onChange={(e) => setReview(e.target.value)}
        />
        <br />
        <div className="review-cups" onMouseLeave={handleMouseLeave}>
          {numbers.map((value) => (
            <div key={value}>
              <i
                className={changeClassName(value)}
                onMouseOver={() => handleMouseOver(value)}
                onClick={() => setCups(value)}
              ></i>
            </div>
          ))}
        </div>
        <div className="new-review-submit-container">
          <button
            id={reviewButton}
            type="submit"
            disabled={disabledButton()}
          >
            Submit Your Review
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateNewReview;
