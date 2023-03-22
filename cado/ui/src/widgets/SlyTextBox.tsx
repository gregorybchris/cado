interface SlyTextBoxProps {
  value: string;
  placeholder: string;
  onBlur: (value: string) => void;
  onChange: (value: string) => void;
}

export default function SlyTextBox(props: SlyTextBoxProps) {
  function onChange(event: any) {
    event.stopPropagation();
    event.preventDefault();
    props.onChange(event.target.value);
  }

  return (
    <input
      className="inline-block bg-transparent outline-none"
      type="text"
      value={props.value}
      placeholder={props.placeholder}
      onBlur={(event) => props.onBlur(event.target.value)}
      onChange={onChange}
    ></input>
  );
}
