__int64 __fastcall sub_1444F9E50(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  _BYTE v6[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6, a3: 1);
  if ( *(_DWORD *)(v4 + 16) == 0
    && (unsigned __int8)sub_14155E4D0(a1, a2) != 0
    && (unsigned __int8)sub_14155E4D0(a1: a1 + 5, a2) != 0
    && (unsigned __int8)sub_14155E4D0(a1: a1 + 10, a2) != 0 )
  {
    return sub_14155E4D0(a1: a1 + 15, a2);
  }
  else
  {
    return 0;
  }
}
