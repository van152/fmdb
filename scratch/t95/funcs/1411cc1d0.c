char __fastcall sub_1411CC1D0(char a1)
{
  char result; // al

  result = 23;
  switch ( a1 )
  {
    case 9:
    case 43:
      return result;
    case 10:
    case 21:
      result = 21;
      break;
    case 11:
    case 36:
      result = 19;
      break;
    case 12:
    case 37:
      result = 18;
      break;
    case 18:
      result = 20;
      break;
    case 29:
      result = 17;
      break;
    case 33:
      result = 22;
      break;
    default:
      result = 100;
      break;
  }
  return result;
}
