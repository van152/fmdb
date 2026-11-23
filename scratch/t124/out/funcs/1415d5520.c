__int64 __fastcall sub_1415D5520(__int64 a1, volatile signed __int32 **a2, char a3, unsigned int a4)
{
  volatile signed __int32 *v4; // rbp
  int v8; // edi
  volatile signed __int32 *v9; // rbp
  __int64 v10; // rsi
  volatile signed __int32 *v11; // rbx
  volatile signed __int32 *v12; // rbx
  volatile signed __int32 *v13; // rdi
  __int64 v14; // rdx
  char v16[41]; // [rsp+2Fh] [rbp-29h] BYREF

  LOBYTE(v4) = 1;
  if ( a3 != 0 )
  {
    v8 = -*(_DWORD *)(a1 - 4);
    v9 = *a2;
    v16[0] = 3;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: v16, a3: 1);
    if ( *((_DWORD *)v9 + 4) != 0 )
      goto LABEL_3;
    v10 = v8 + a1;
    LODWORD(v4) = 0;
    if ( (unsigned __int8)sub_140E089C0(a1: v10 - 240, a2, a3: 0, a4) != 0 )
    {
      LODWORD(v4) = 0;
      if ( (unsigned __int8)sub_140DC40F0(a1: v10, a2, a3: 0, a4) != 0 )
      {
        LODWORD(v4) = 0;
        if ( (unsigned __int8)sub_140DDADF0(a1: v10 + 376, a2, a3: 0, a4) != 0 )
        {
          LODWORD(v4) = 0;
          if ( (unsigned __int8)sub_140DFC460(a1: v10 + 160, a2, a3: 0, a4) != 0 )
          {
            v11 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: v10 + 24,
              a3: 8);
            if ( *((_DWORD *)v11 + 4) != 0 )
              goto LABEL_3;
            v12 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: v10 + 8,
              a3: 4);
            if ( *((_DWORD *)v12 + 4) != 0 )
              goto LABEL_3;
            v4 = *a2;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: v10 + 12,
              a3: 4);
            if ( *((_DWORD *)v4 + 4) != 0 )
              goto LABEL_3;
            v13 = *a2;
            v14 = *(_DWORD *)(v10 + 16) != 0 ? v10 + 16 : v10 + 12;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
              a1: *a2,
              a2: v14,
              a3: 4);
            LOBYTE(v4) = 1;
            if ( *((_DWORD *)v13 + 4) != 0 )
LABEL_3:
              LODWORD(v4) = 0;
          }
        }
      }
    }
  }
  return (unsigned int)v4;
}
