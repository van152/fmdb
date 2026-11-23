__int64 __fastcall sub_144530E00(__int64 a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rbp
  unsigned int v12; // ebp
  _DWORD v14[10]; // [rsp+40h] [rbp-28h] BYREF

  sub_140814B10(*a2, v14, a1 + 24);
  if ( v14[0] != 0 )
    return 0;
  sub_140814B10(*a2, v14, a1 + 32);
  if ( v14[0] != 0 )
    return 0;
  sub_140814B10(*a2, v14, a1 + 40);
  if ( v14[0] != 0 )
    return 0;
  sub_140814B10(*a2, v14, a1 + 48);
  if ( v14[0] != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  sub_141580170(v14, a2, a1 + 64);
  if ( v14[0] != 0 )
  {
    return 0;
  }
  else
  {
    v12 = 0;
    if ( (unsigned __int8)sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0 )
    {
      sub_14157F860(a1);
      LOBYTE(v12) = 1;
    }
  }
  return v12;
}
