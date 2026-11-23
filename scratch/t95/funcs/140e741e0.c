__int64 __fastcall sub_140E741E0(__int64 a1)
{
  __int64 *v1; // rax
  __int64 v2; // rax
  __int64 v3; // rsi
  __int64 v4; // rcx
  __int64 v5; // rcx

  v1 = *(__int64 **)(a1 + 24);
  if ( v1 == *(__int64 **)(a1 + 32) )
    return 0;
  v2 = *v1;
  if ( v2 == 0 )
    return 0;
  v3 = *(_QWORD *)(v2 + 128);
  if ( v3 == 0 )
    return 0;
  v4 = v3 + *(int *)(*(_QWORD *)(v3 + 8) + 4LL) + 8;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v4 + 528LL))(v4) == 0 )
    return 0;
  v5 = v3 + *(int *)(*(_QWORD *)(v3 + 8) + 4LL) + 8;
  return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v5 + 1752LL))(v5);
}
