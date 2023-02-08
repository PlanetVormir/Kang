import { useState } from "react";

interface StudentInterface {
  fullName: string;
  motherName: string;
  fatherName: string;
  rollNo: number;
}

const GetDetailsForm = (): JSX.Element => {
  const [student, setStudent] = useState({
    fullName: "",
    motherName: "",
    fatherName: "",
    rollNo: 0,
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    
  };

  return (
    <div className="get-details-form w-full lowercase mt-24">
      <h1 className="font-bold text-3xl text-center my-3">
        get the marks of your entire batch
      </h1>
      <form className="mx-auto" method="post">
        <input
          className="w-full rounded text-lg p-2 my-2"
          placeholder="full name"
          name="name"
          onChange={(e) => handleChange(e)}
          value={student.fullName}
        ></input>
        <div className="w-full my-2 grid grid-cols-2 gap-2">
          <input
            className="p-2 rounded"
            placeholder="father's name"
            name="fatherName"
          ></input>
          <input
            className="p-2 rounded"
            placeholder="mother's name"
            name="motherName"
          ></input>
        </div>

        <input
          className="w-full rounded text-lg p-2 my-2"
          placeholder="boards roll no"
          name="rollNo"
        ></input>

        <button
          className="w-full bg-blue-500 rounded p-2 my-2 text-lg"
          type="submit"
        >
          submit
        </button>
      </form>
    </div>
  );
};

export default GetDetailsForm;
