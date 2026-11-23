// THUNK ALIAS -> sub_1443AF0F0 (jmp:0x14147bd40->0x1443af0f0)
bool __fastcall sub_1443AF0F0(int a1, __int16 a2, char a3)
{
  int v3; // r9d
  int v4; // eax
  int v5; // edx
  bool result; // al

  v3 = a2;
  if ( (unsigned int)(a3 - 2) >= 3 )
  {
    if ( a3 == 1 )
    {
      v4 = 10;
    }
    else if ( a3 != 0 )
    {
      v4 = 6;
    }
    else
    {
      v4 = (a2 >= 9001) | 6;
    }
  }
  else
  {
    v4 = 7;
  }
  v5 = v4 * a2 * a2;
  result = true;
  if ( v5 <= a1 )
    return v3 < 500 && a1 < 100000;
  return result;
}
