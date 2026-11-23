// THUNK ALIAS -> sub_1444CEDA0 (jmp:0x141532ab0->0x1444ceda0)
__int64 __fastcall sub_1444CEDA0(__int64 a1, __int64 a2, char a3)
{
  __int64 v6; // rax
  __int64 v7; // rax
  __int64 v8; // rdx
  __int64 v9; // rsi
  unsigned __int64 i; // rcx
  __int64 v11; // rdi
  int v12; // edx

  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_QWORD *)a1 = 0;
  *(_QWORD *)(a1 + 24) = a2;
  *(_QWORD *)(a1 + 32) = 0;
  *(_BYTE *)(a1 + 40) = a3;
  v6 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_7;
  while ( *(_DWORD *)v6 != 1986359923 )
  {
    v6 += 16;
    if ( v6 == qword_141B60C38 )
      goto LABEL_7;
  }
  if ( v6 == qword_141B60C38 || *(_QWORD *)(v6 + 8) == 0 )
  {
LABEL_7:
    sub_140E6EAC0(a2);
    v7 = *(_QWORD *)(a1 + 24);
    v8 = *(_QWORD *)(v7 + 280);
    v9 = *(_QWORD *)(v7 + 288);
    if ( v9 != v8 )
    {
      for ( i = 0; i < (v9 - v8) >> 3; ++i )
      {
        v11 = *(_QWORD *)(v8 + 8 * i);
        if ( v11 != 0 )
        {
          v12 = *(unsigned __int8 *)(v11 + 48);
          if ( (unsigned int)(v12 - 4) >= 5 && v12 != 20 )
            return a1;
          ++*(_QWORD *)(a1 + 32);
          v8 = *(_QWORD *)(v7 + 280);
          v9 = *(_QWORD *)(v7 + 288);
        }
      }
    }
  }
  return a1;
}
