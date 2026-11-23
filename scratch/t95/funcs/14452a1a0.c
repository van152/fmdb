__int64 __fastcall sub_14452A1A0(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  volatile signed __int32 *v11; // rsi
  volatile signed __int32 *v12; // rsi

  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 368, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 376, 1);
  if ( *((_DWORD *)v12 + 4) != 0 || (unsigned __int8)sub_140E5B1A0(a1, (__int64 *)a2, 0, a4, a5, a6, a7, a8) == 0 )
    return 0;
  else
    return sub_1411D1730(a1, a2, 0, a4, a5, a6, a7, a8);
}
