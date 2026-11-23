// THUNK ALIAS -> sub_143C53CD0 (jmp:0x140e7e710->0x143c53cd0)
__int64 __fastcall sub_143C53CD0(__int64 a1)
{
  _BYTE *v1; // rsi
  char v2; // al

  v1 = *(_BYTE **)(a1 + 336);
  if ( v1 != nullptr )
  {
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)v1 + 56LL))(*(_QWORD *)(a1 + 336)) == 1 )
    {
      v2 = v1[2229];
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v1 + 1136LL))(v1) != 0 )
    {
      v2 = (*(__int64 (__fastcall **)(_BYTE *))(*(_QWORD *)v1 + 1136LL))(v1);
    }
    else
    {
      v2 = sub_141485D40(v1);
    }
    LOBYTE(a1) = 1;
    if ( v2 <= 15 )
    {
      LOBYTE(a1) = 2;
      if ( v2 <= 12 )
      {
        LOBYTE(a1) = 3;
        if ( v2 <= 9 )
        {
          LOBYTE(a1) = 4;
          if ( v2 <= 5 )
          {
            LOBYTE(a1) = 5;
            if ( v2 <= 2 )
              LOBYTE(a1) = (v2 > 0) ^ 7;
          }
        }
      }
    }
  }
  else
  {
    LOBYTE(a1) = 7;
  }
  return (unsigned int)a1;
}
