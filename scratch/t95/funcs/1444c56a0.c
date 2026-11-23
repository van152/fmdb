char __fastcall sub_1444C56A0(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  _DWORD v5[4]; // [rsp+28h] [rbp-10h] BYREF

  result = 0;
  if ( a2 > 1768386158 )
  {
    if ( a2 == 1768386159 )
    {
      *(_BYTE *)(a1 + 36) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
    }
    else
    {
      if ( a2 != 1885696611 )
        return result;
      *(float *)(a1 + 32) = (*(float (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
    }
  }
  else if ( a2 == 1181639028 )
  {
    sub_140FE7960(v5, a3, 0);
    *(_DWORD *)(a1 + 24) = v5[0];
  }
  else
  {
    if ( a2 != 1399742836 )
      return result;
    sub_140FE7960(v5, a3, 0);
    *(_DWORD *)(a1 + 28) = v5[0];
  }
  return 1;
}
