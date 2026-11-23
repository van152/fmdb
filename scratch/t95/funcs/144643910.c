__int64 __fastcall sub_144643910(__int64 *a1)
{
  __int64 v2; // rdi
  __int64 v3; // rax
  __int64 v4; // r8

  if ( dword_141B5FBD0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5FBD0);
    if ( dword_141B5FBD0 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5FB80, 1100122305, 5000, 80, 0, 1, 5000, 4096);
      sub_141751048(sub_140FB4420);
      sub_141750EA0(&dword_141B5FBD0);
    }
  }
  v2 = sub_1407E58C0(&unk_141B5FB80, 80);
  v3 = *a1;
  *(_QWORD *)(v2 + 8) = -1;
  *(_DWORD *)(v2 + 16) = 0;
  *(_QWORD *)v2 = 0x1418BE628LL;
  *(_QWORD *)(v2 + 24) = 0;
  *(_QWORD *)(v2 + 32) = v3;
  *(_QWORD *)(v2 + 64) = 0;
  *(_QWORD *)(v2 + 56) = 0;
  *(_QWORD *)(v2 + 48) = 0;
  *(_QWORD *)(v2 + 40) = 0;
  *(_DWORD *)(v2 + 72) = 124520300;
  *(_WORD *)(v2 + 76) = 0;
  *(_BYTE *)(v2 + 78) = -1;
  *(_DWORD *)(v2 + 12) = *(_DWORD *)(qword_141B60158 + 80) + 1;
  LOBYTE(v4) = (_BYTE)word_141B60460 != 6;
  sub_140F6C770(qword_141B60158, v2, v4);
  return v2;
}
