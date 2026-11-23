bool __fastcall sub_1445044E0(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v8; // rsi
  __int64 v9; // rsi
  _DWORD *v10; // rdi
  __int64 v11; // rdx
  bool result; // al
  _BYTE v13[33]; // [rsp+27h] [rbp-21h] BYREF

  v7 = (_DWORD *)*a2;
  v13[0] = 0;
  (*(void (__fastcall **)(_DWORD *, _BYTE *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v13, 1);
  result = false;
  if ( v7[4] == 0 && (a4 == 0 || (unsigned __int8)sub_1409FAA20(a1 + 24, a2) != 0) )
  {
    v8 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
    if ( v8[4] == 0 )
    {
      v9 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
      if ( *(_DWORD *)(v9 + 16) == 0 )
      {
        v10 = (_DWORD *)*a2;
        v11 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, v11, 4);
        if ( v10[4] == 0 )
          return true;
      }
    }
  }
  return result;
}
