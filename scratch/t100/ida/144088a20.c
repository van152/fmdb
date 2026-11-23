__int64 __fastcall sub_144088A20(__int64 a1)
{
  __int64 v1; // rsi
  __int64 v2; // rdi
  __int64 v3; // rbx
  __int64 v4; // r14
  __int64 (__fastcall *v5)(__int64); // r15
  __int64 v6; // rcx
  unsigned int v7; // eax
  __int64 v8; // rcx
  __int64 v9; // rax

  v1 = a1;
  v2 = qword_141AC0410;
  if ( qword_141AC0410 == 0 )
  {
    a1 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
    if ( dword_141AC0408 > *(_DWORD *)(a1 + 4) )
    {
      sub_141750E08(&dword_141AC0408);
      if ( dword_141AC0408 == -1 )
      {
        if ( qword_141AC0410 == 0 )
        {
          byte_141AC0418 = 1;
          qword_141AC0410 = sub_14121A790(a1);
          byte_141AC0418 = 0;
        }
        sub_141751048(sub_140EA4B50);
        sub_141750EA0(&dword_141AC0408);
      }
    }
    v2 = qword_141AC0410;
    if ( qword_141AC0410 == 0 )
    {
      byte_141AC0418 = 1;
      v2 = sub_14121A790(a1);
      qword_141AC0410 = v2;
      byte_141AC0418 = 0;
    }
  }
  *(_QWORD *)v1 = 0;
  *(_WORD *)(v1 + 8) = 0;
  v3 = qword_141B59FA0;
  if ( qword_141B59FA0 != 0 )
  {
    v4 = *(_QWORD *)(qword_141B59FA0 + 16);
    v5 = MEMORY[0x141947498];
    *(_BYTE *)(v1 + 8) = v4 == (unsigned int)MEMORY[0x141947498](a1);
    v7 = v5(v6);
    v8 = *(_QWORD *)(v3 + 16);
    if ( v8 == 0 || v8 == v7 )
    {
      *(_QWORD *)(v3 + 16) = v7;
      *(_BYTE *)(v1 + 9) = 1;
      v9 = *(_QWORD *)(v3 + 8);
      *(_QWORD *)v1 = v9;
      if ( v2 != 0 )
        *(_QWORD *)(v3 + 8) = v2;
      else
        *(_QWORD *)(v3 + 8) = v9;
    }
    else
    {
      *(_BYTE *)(v1 + 9) = 0;
    }
  }
  return v1;
}
