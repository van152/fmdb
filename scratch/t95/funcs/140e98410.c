__int64 __fastcall sub_140E98410(__int64 a1, unsigned __int8 a2, unsigned int a3, __int64 a4)
{
  __int64 v4; // rax
  __int64 v5; // rbx
  __int64 v8; // rdx
  __int64 v9; // rax

  v4 = *(_QWORD *)(a1 + 24);
  if ( (int)(((unsigned __int64)(*(_QWORD *)(a1 + 32) - v4) >> 3) - 1) < a2 )
    return 0;
  v5 = *(_QWORD *)(v4 + 8LL * a2);
  if ( v5 == 0 )
    return 0;
  v8 = *(unsigned int *)(v5 + 12);
  if ( (_DWORD)v8 == -1 || (v9 = sub_140F45DB0(qword_141B5FDB8, v8)) == 0 )
    v9 = *(_QWORD *)(v5 + 48);
  if ( v9 != 0 )
    return (*(__int64 (__fastcall **)(__int64, _QWORD, __int64))(*(_QWORD *)v9 + 16LL))(v9, a3, a4);
  else
    return 0;
}
