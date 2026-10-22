
import csv
from datetime import datetime, date

info = []
objects = []
today = date.today()


try:
    with open("orders.csv", "r", newline="", encoding="utf-8") as file:
        data = csv.DictReader(file)

        for line in data:
            info.append(line)

except FileNotFoundError:
    print("courses.csv does not exist")
    raise SystemExit


class Course:
    def __init__(self, CourseID, CourseName, BaseFee,
                 OfferDiscount, OfferEndDate):
        self.CourseID = CourseID
        self.CourseName = CourseName
        self.BaseFee = BaseFee
        self.OfferDiscount = OfferDiscount
        self.OfferEndDate = OfferEndDate

    def fee_calculation(self):
        raise NotImplementedError

    def calculate_details(self):
        adjusted_fee = self.fee_calculation()

        if (
            self.OfferDiscount > 0
            and self.OfferEndDate is not None
            and self.OfferEndDate >= today
        ):
            offer_amount = adjusted_fee * self.OfferDiscount / 100
            final_fee = adjusted_fee - offer_amount
            offer_status = "WithOffer"
        else:
            offer_amount = 0
            final_fee = adjusted_fee
            offer_status = "WithoutOffer"

        return adjusted_fee, offer_amount, final_fee, offer_status


class ClassroomCourse(Course):
    def fee_calculation(self):
        return self.BaseFee + 2000


class OnlineCourse(Course):
    def fee_calculation(self):
        return self.BaseFee * 0.90


def validation(info):
    valid = []
    errors = []
    valid_course_id = set()

    for line in info:
        try:
            course_id = line["CourseID"].strip()
            course_name = line["CourseName"].strip()
            course_type = line["CourseType"].strip()
            base_fee = float(line["BaseFee"])
            offer_discount = float(line["OfferDiscount"])
            date_value = line["OfferEndDate"].strip()

            if course_id == "":
                raise ValueError("Course ID is empty")

            if course_id in valid_course_id:
                raise ValueError("Duplicate Course ID")

            if course_name == "":
                raise ValueError("Course name is empty")

            if course_type not in ["Classroom", "Online"]:
                raise ValueError("Invalid Course Type")

            if base_fee <= 0:
                raise ValueError("Base fee must be greater than zero")

            if not 0 <= offer_discount <= 100:
                raise ValueError("Offer discount must be between 0 and 100")

            if date_value == "":
                offer_end_date = None
            else:
                offer_end_date = datetime.strptime(
                    date_value, "%Y-%m-%d"
                ).date()

                if offer_end_date.strftime("%Y-%m-%d") != date_value:
                    raise ValueError("Date must be YYYY-MM-DD")

            line["CourseID"] = course_id
            line["CourseName"] = course_name
            line["CourseType"] = course_type
            line["BaseFee"] = base_fee
            line["OfferDiscount"] = offer_discount
            line["OfferEndDate"] = offer_end_date

            valid.append(line)
            valid_course_id.add(course_id)

        except (ValueError, TypeError, KeyError) as e:
            errors.append({
                "Record": str(line),
                "Reason": str(e)
            })

    return valid, errors


valid, errors = validation(info)


def object_creation(valid):
    objects = []

    for line in valid:
        if line["CourseType"] == "Classroom":
            obj = ClassroomCourse(
                line["CourseID"],
                line["CourseName"],
                line["BaseFee"],
                line["OfferDiscount"],
                line["OfferEndDate"]
            )
        else:
            obj = OnlineCourse(
                line["CourseID"],
                line["CourseName"],
                line["BaseFee"],
                line["OfferDiscount"],
                line["OfferEndDate"]
            )

        objects.append(obj)

    return objects


objects = object_creation(valid)

report = []
total_fees = 0

for obj in objects:
    adjusted_fee, offer_amount, final_fee, offer_status = (
        obj.calculate_details()
    )

    total_fees += final_fee

    if obj.OfferEndDate is None:
        offer_date = ""
    else:
        offer_date = obj.OfferEndDate.strftime("%Y-%m-%d")

    if isinstance(obj, ClassroomCourse):
        adjustment_amount = 2000
    else:
        adjustment_amount = obj.BaseFee * 0.10

    row = {
        "CourseID": obj.CourseID,
        "CourseName": obj.CourseName,
        "CourseType": (
            "Classroom"
            if isinstance(obj, ClassroomCourse)
            else "Online"
        ),
        "BaseFee": f"{obj.BaseFee:.2f}",
        "CourseAdjustmentFee": f"{adjustment_amount:.2f}",
        "OfferDiscountPercent": f"{obj.OfferDiscount:g}",
        "OfferEndDate": offer_date,
        "OfferStatus": offer_status,
        "OfferDiscountAmount": f"{offer_amount:.2f}",
        "FinalFee": f"{final_fee:.2f}"
    }

    report.append(row)

    print(
        f"{obj.CourseID}, {obj.CourseName}, "
        f"Adjusted Fee: ₹{adjusted_fee:.2f}, "
        f"{offer_status}, "
        f"Offer Discount: ₹{offer_amount:.2f}, "
        f"Final Fee: ₹{final_fee:.2f}"
    )


fieldnames = [
    "CourseID",
    "CourseName",
    "CourseType",
    "BaseFee",
    "CourseAdjustmentFee",
    "OfferDiscountPercent",
    "OfferEndDate",
    "OfferStatus",
    "OfferDiscountAmount",
    "FinalFee"
]

with open(
    "course_fee_report.csv", "w", newline="", encoding="utf-8"
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report)


with open("errors.txt", "w", encoding="utf-8") as file:
    for error in errors:
        file.write(
            f"Record: {error['Record']}\n"
            f"Reason: {error['Reason']}\n\n"
        )


print("\n----- FINAL SUMMARY -----")
print("Total valid courses:", len(objects))
print("Total rejected records:", len(errors))
print(f"Combined final fees: ₹{total_fees:.2f}")
print("Report saved to course_fee_report.csv")
print("Rejected records saved to errors.txt")
