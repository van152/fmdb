char __fastcall sub_1444C4780(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  _DWORD v5[4]; // [rsp+28h] [rbp-10h] BYREF

  result = 0;
  if ( a2 > 1851880552 )
  {
    if ( a2 == 1918989417 )
    {
      *(_BYTE *)(a1 + 32) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    else
    {
      if ( a2 != 1851880553 )
        return result;
      sub_140FE7960(v5, a3, 0);
      *(_DWORD *)(a1 + 28) = v5[0];
    }
  }
  else if ( a2 == 1835104353 )
  {
    *(_BYTE *)(a1 + 34) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
  }
  else
  {
    if ( a2 != 1835626081 )
      return result;
    *(_BYTE *)(a1 + 33) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
  }
  return 1;
}
