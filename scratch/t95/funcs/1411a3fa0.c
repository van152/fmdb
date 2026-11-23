__int64 __fastcall sub_1411A3FA0(__int64 a1)
{
  __int64 v1; // rsi
  __int64 v2; // rcx
  __int64 v3; // rcx

  v1 = *(_QWORD *)(a1 + 128);
  if ( v1 == 0 )
    return 0;
  v2 = v1 + *(int *)(*(_QWORD *)(v1 + 8) + 4LL) + 8;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v2 + 528LL))(v2) == 0 )
    return 0;
  v3 = v1 + *(int *)(*(_QWORD *)(v1 + 8) + 4LL) + 8;
  return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 1752LL))(v3);
}
