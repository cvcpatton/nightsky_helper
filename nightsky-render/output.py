from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Observation(db.Model):
    __tablename__ = "observations"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    moon_phase = db.Column(db.String)
    visibility_score = db.Column(db.Float)
    notes = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "moon_phase": self.moon_phase,
            "visibility_score": self.visibility_score,
            "notes": self.notes,
        }

    @classmethod
    def from_calculation(cls, calculation_result):
        """
        Expects whatever SkyCalculator.calculate() returns.
        Adjust keys if needed.
        """
        return cls(
            date=calculation_result.date,
            moon_phase=calculation_result.moon_phase,
            visibility_score=calculation_result.visibility_score,
            notes=calculation_result.notes,
        )
